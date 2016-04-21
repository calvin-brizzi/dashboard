import requests
import sys
import re
from config import config

EMAIL = ''
PASSWORD = ''

URL = 'https://clientzone.afrihost.com/en/login_check'

def afrihost_data():
    # Start a session so we can have persistent cookies
    session = requests.session()

    # This is the form data that the page sends when logging in
    login_data = {
        '_username': config["email"],
        '_password': config["afrihost"]["pass"],
        'submit': 'login_check',
    }

    # Authenticate
    r = session.post(URL, data=login_data)

    # Access page
    r = session.get('https://clientzone.afrihost.com/en/my-connectivity')
    text = r.text
    
    # Remove all the html, strip all whitespace
    text = re.sub('<[^<]+?>', '', text)
    text = re.sub(r'\s+', '', text)
    
    # Get percentage and gb remaining
    percentage = re.search(r'(\d\d)%USED', text).group(1)
    remaining = re.search(r'(\d*\.\d)GBREMAINING',  text).group(1)
 
    return {
		"percentage": int(percentage),
		"remaining" : float(remaining) - 1,
	}

if __name__ == '__main__':
    afrihost_data()
