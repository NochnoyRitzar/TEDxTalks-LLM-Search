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


def parse_talk_transcript(transcript_section):
    """
    Join transcript string into a single text

    :param transcript_section: response content containing transcript data
    :return: transcript of a talk
    """
    transcript_data = transcript_section.get("translation")
    # check if talk has no transcript
    if not transcript_data:
        return ''
    paragraphs_list = transcript_data.get("paragraphs")
    text_list = []
    for paragraph in paragraphs_list:
        cues = paragraph.get('cues')
        paragraph_text = [cue.get('text').replace('\n', ' ') for cue in cues]
        text_list.append(' '.join(paragraph_text))

    transcript = ' '.join(text_list)

    return transcript


def parse_talk_page_data(json_content):
    video_data = json_content.get("props", {}).get("pageProps", {}).get("videoData", {})
    player_data = json.loads(video_data.get("playerData"))

    event = player_data.get("event")

    talk_data = {
        '_id': video_data['id'],
        'title': video_data['title'],
        'duration': video_data['duration'],
        'views': video_data['viewedCount'],
        'summary': video_data['description'],
        'event': event,
        'recorded_date': video_data['recordedOn'],
        'published_date': video_data['publishedAt'],
        'topics': [
            {'id': topic['id'], 'name': topic['name']} for topic in video_data.get("topics", {}).get("nodes")
        ],
        'speakers': [
            {
                'name': ' '.join([speaker['firstname'], speaker['lastname']]).strip(),
                'occupation': 'Educator' if event == 'TED-Ed' else speaker['description']
            } for speaker in video_data.get("speakers", {}).get("nodes")
        ],
        'subtitle_languages': [
            {
                'name': language['languageName'],
                'code': language['languageCode']
            } for language in player_data.get("languages")
        ],
        'youtube_video_code': player_data.get('external', {}).get('code'),
        'related_videos': [video['id'] for video in video_data['relatedVideos']],
        'transcript': parse_talk_transcript(json_content.get("props", {}).get("pageProps", {}).get("transcriptData", {}))
    }

    return talk_data


if __name__ == "__main__":
    url = "https://www.ted.com/talks/ali_abu_awwad_and_ami_dar_an_israeli_and_a_palestinian_talk_peace_dignity_and_safety/transcript"
    next_data_content = find_next_data_script(url)
    if next_data_content:
        talk_data = parse_talk_page_data(next_data_content)
        print(talk_data)
    else:
        print("Could not find the __NEXT_DATA__ script tag.")