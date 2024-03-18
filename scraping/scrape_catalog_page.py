import json
import requests
from bs4 import BeautifulSoup
from google.cloud import bigquery


def get_page_content(url):
    response = requests.get(url)
    response.raise_for_status()  # Raise an HTTPError for bad responses

    return response.text


def find_next_data_script(page_content):
    """
    Fetches the HTML content from the given URL, parses it to find the <script id="__NEXT_DATA__"> tag,
    and returns its content.

    :param page_content: URL of the webpage to parse
    :return: Content of the <script id="__NEXT_DATA__"> tag or None if not found
    """
    try:
        # Parse the HTML content
        soup = BeautifulSoup(page_content, 'html.parser')

        # Find the <script id="__NEXT_DATA__"> tag
        script_tag = soup.find('script', id='__NEXT_DATA__')

        if script_tag:
            script_content = json.loads(script_tag.string)
            return script_content
        else:
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def parse_catalog_page_data(json_content):
    talks_list = json_content.get("props", {}).get("pageProps", {}).get("talks", [])
    # Can use those ids for filtering if they are unique
    ids_list = [int(json.loads(talk.get("playerData")).get("id")) for talk in talks_list]

    return ids_list


def query_bigquery(talk_ids):
    """
    Queries the BigQuery database to identify missing talks
    :param talk_ids: catalog page talks ids
    :return:
    """
    client = bigquery.Client()

    # Create a string with comma-separated talk IDs for the query
    talk_ids_str = ",".join(f"'{id}'" for id in talk_ids)

    # Query to find which of the provided talk_ids are not in the BigQuery table
    query = f"""
        SELECT page_id
        FROM `ted-talks-rec.ted_talks_dataset.talks_data`
        WHERE page_id IN ({talk_ids_str})
    """
    query_job = client.query(query)

    # Determine which IDs are missing by comparing with the list of page_ids present in BigQuery
    existing_ids = [row.page_id for row in query_job]
    missing_ids = [page_id for page_id in talk_ids if page_id not in existing_ids]

    return missing_ids


def main():
    url = "https://www.ted.com/talks?sort=newest"
    page_content = get_page_content(url)
    next_data_content = find_next_data_script(page_content)
    if next_data_content:
        ids_list = parse_catalog_page_data(next_data_content)
        missing_talk_ids = query_bigquery(ids_list)
        print(missing_talk_ids)
    else:
        print("Could not find the __NEXT_DATA__ script tag.")


if __name__ == "__main__":
    main()