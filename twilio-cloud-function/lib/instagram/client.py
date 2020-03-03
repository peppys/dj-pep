import json
import logging
import re
from typing import Dict

import requests

from bs4 import BeautifulSoup


def fetch_instagram_profile(username: str) -> Dict:
    """
    Scrapes instagram profile information via website
    :param username:
    :return:
    """
    try:
        response = requests.get(f'https://www.instagram.com/{username}/')
        response.raise_for_status()
    except Exception as e:
        logging.error(f'Unable to fetch instagram page for username {username}: {e}')
        raise e

    soup = BeautifulSoup(response.content, 'html.parser')
    data_script = soup.find('script', type="text/javascript", text=re.compile('window._sharedData'))

    profile_json_string = data_script.get_text().replace('window._sharedData = ', '')[:-1]
    profile_json = json.loads(profile_json_string)
    profile_data = profile_json['entry_data']['ProfilePage'][0]['graphql']['user']

    return {
        'username': profile_data['username'],
        'full_name': profile_data['full_name'],
        'bio': profile_data['biography'],
        'followers_count': profile_data['edge_followed_by']['count'],
        'following_count': profile_data['edge_follow']['count'],
    }
