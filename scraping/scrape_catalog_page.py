import json
import requests
from bs4 import BeautifulSoup


def find_next_data_script(url):
    """
    Fetches the HTML content from the given URL, parses it to find the <script id="__NEXT_DATA__"> tag,
    and returns its content.

    :param url: URL of the webpage to parse
    :return: Content of the <script id="__NEXT_DATA__"> tag or None if not found
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses

        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

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


if __name__ == "__main__":
    url = "https://www.ted.com/talks?sort=newest"
    next_data_content = find_next_data_script(url)
    if next_data_content:
        ids_list = parse_catalog_page_data(next_data_content)
        print(ids_list)
    else:
        print("Could not find the __NEXT_DATA__ script tag.")