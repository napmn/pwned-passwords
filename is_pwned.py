import hashlib
import requests
import sys
from getpass import getpass


def request_pwdnedpasswords(hashed_passwd):
    """
    Fetches pwdnedpasswords.com API with the first 5 characters
    of the hashed string and calls funtion to parse response.

    Parameters
    ----------
    hashed_passwd: str
        password hashed by SHA-1
    """
    response = requests.get('https://api.pwnedpasswords.com/range/{}'.format(
            hashed_passwd[0:5]))
    if not response.ok:
        print('Could not fetch pwnedpasswords.com')
        return
    parse_response(response.text, hashed_passwd)


def parse_response(response_text, hashed_passwd):
    """
    Parses response from pwdnedpasswords.com and search
    for a match with hashed password.

    Parameters
    ----------
    response_text: str
        text of the response
    hashed_passwd: str
        password hashed by SHA-1
    """
    second_part = hashed_passwd[5:].upper()
    lines = response_text.split('\r\n')
    for line in lines:
        splitted = line.split(':')
        if splitted[0] == second_part:
            print('Password has been pwned {} times.'.format(splitted[1]))
            break
    else:
        print('Password has not been pwned so far.')


if __name__ == '__main__':
    passwd = getpass()
    hashed_passwd = hashlib.sha1(passwd .encode('utf-8')).hexdigest()
    request_pwdnedpasswords(hashed_passwd)
