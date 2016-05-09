import logging
import requests
import urllib2
from config import config

log = logging.getLogger(__name__)

BASE_URL = "https://myvodacom.secure.vodacom.co.za/rest/services/v1/"
LOGIN_URL = BASE_URL + "context/loginUser/%s"
BUNDLE_BALANCES_URL = BASE_URL + "bundlebalances/getbundlebalances"
CONTEXT_URL = BASE_URL + "context/set/%s"

def vodacom_data():
    user = config["email"]
    password = config["vodacom"]["pass"]
    phone_number = config["vodacom"]["cell"]

    post_headers = {
        'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:39.0) Gecko/20100101 Firefox/39.0",
        'Accept': "application/json, text/plain, */*",
        'Accept-Language': "en-US,en;q=0.5",
        'DNT': "1",
        'Content-Type': "application/x-www-form-urlencoded; charset=UTF-8",
        'Referer': "https://myvodacom.secure.vodacom.co.za/vodacom/log-in?intendedURL=http%3A%2F%2Fmyvodacom."
                   "secure.vodacom.co.za%2Fvodacom%2Fmyvodacom%2Fmy-summary",
        'Pragma': "no-cache",
        'Cache-Control': "no-cache"
    }

    data = {
        'password': password,
        'mobile': "false",
        'referer': "https://myvodacom.secure.vodacom.co.za/vodacom/log-in",
        'currentUrl': "https://myvodacom.secure.vodacom.co.za/vodacom/log-in"
    }

    session = requests.Session()
    log.info("sending login request")
    r = session.post(LOGIN_URL % user, data=data, headers=post_headers)

    if r.status_code != 200:
        raise urllib2.HTTPError(r.request.url, r.status_code, "Login request failed.", {}, None)

    data = r.json()
    if not data['successfull']:
        error_messages = map(lambda m: m['message'], filter(lambda m: m['errorMessage'], data['messages']))
        raise ValueError("Login request failed. " + "; ".join(error_messages))

        """
        Get the balances for each service type associated with each phone number.

        :return: nested dictionary. phone number -> services* -> name, description, remaining, unit
        """
    log.info("switching context to %s.", phone_number)
    r = session.post(CONTEXT_URL % phone_number,
                          data={"tracker": "numberDropdownMainTracker"}, headers=post_headers)
    if r.status_code != 200:
        raise urllib2.HTTPError(r.request.url, r.status_code, "Context switch request failed.", {}, None)
        log.info("getting bundle balances.")
    r = session.get(BUNDLE_BALANCES_URL)
    if r.status_code != 200:
        raise urllib2.HTTPError(r.request.url, r.status_code, "Bundle balances request failed.", {}, None)
    data = r.json()
    services = {}
    for service in data['bundleBalances'].get('serviceTypesList', []):
        services[service['name']] = {
            'remaining': service['totalRemaining'],
            'unit': service['unit'].lower()
        }

    return services
