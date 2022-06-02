from base64 import b64encode
from time import sleep

from bs4 import BeautifulSoup
from requests_html import HTMLSession

from config.configservice import ConfigService


def send_to_spamcop(mail_content):
    """
    Fill the report for every mail.
    """
    print("  > connecting to SpamCop")

    # get form
    session = HTMLSession()
    res = send_get(session, ConfigService.get('SPAM_URL'))
    first_form = get_all_forms(res)[0]
    # get action
    action = first_form.attrs.get("action").lower()
    # get current form
    post_params = get_prefill(first_form)
    # add mail content to text
    post_params['spam'] = mail_content
    # don't verbose
    # post_params['verbose'] = '0'

    # send the spam!
    print("  ~ sending spam")
    post_url = ConfigService.get('SPAM_URL') + action
    response = send_post(session, post_url, post_params)

    # get response
    send_get(session, response.url)
    # wait a little bit (un-fuelled version)
    wait(7)

    # get the new page (after nag screen)
    res = send_get(session, response.url)
    first_form = get_all_forms(res)[0]
    action = first_form.attrs.get("action").lower()
    post_params = get_prefill(first_form)

    # process final report validation
    print("  ~ filling spam report")
    post_url = ConfigService.get('SPAM_URL') + action
    send_post(session, post_url, post_params)
    print("  ~ done")


def send_get(session, url):
    """Send GET request to specified URL"""
    # configure basic auth.
    headers = get_headers()

    # create session, connect to website
    res = session.get(url, headers=headers)

    # if error
    if not res.ok:
        raise Exception('not connected!', res)

    # for javascript driven website
    # res.html.render()

    # closing connection!
    res.close()

    return res


def send_post(session, url, post_params):
    """Send POST request to specified URL"""
    # configure basic auth.
    headers = get_headers()

    # create session, connect to website
    res = session.post(url, headers=headers, data=post_params)

    # if error
    if not res.ok:
        raise Exception('not connected!', res)

    # for javascript driven website
    # res.html.render()

    # closing connection!
    res.close()

    return res


def get_all_forms(res):
    """Returns all forms tags found webpage"""
    soup = BeautifulSoup(res.html.html, "html.parser")
    forms = soup.find_all("form")
    return forms


def get_prefill(form):
    """Returns input and text areas from HTML form with their values"""
    # get the form action (requested URL)
    form.attrs.get("action").lower()

    # get all form inputs
    inputs = {}
    for input_tag in form.find_all("input"):
        name = input_tag.attrs.get("name")
        value = input_tag.attrs.get("value", "")
        inputs[name] = value
    for input_tag in form.find_all("textarea"):
        name = input_tag.attrs.get("name")
        value = input_tag.attrs.get("value", "")
        inputs[name] = value
    return inputs


def wait(seconds):
    """Wait for the required amount of time"""
    print('  - wait %d seconds' % seconds, end='', flush=True)
    for x in range(0, seconds):
        sleep(1)
        print('.', end='', flush=True)
    print('')


def get_headers():
    """Create the basic auth header"""
    user_and_pass = b64encode(bytes(ConfigService.get('SPAM_LOGIN_PASSWD'), "utf-8")).decode("utf-8")
    return {'Authorization': 'Basic %s' % user_and_pass}
