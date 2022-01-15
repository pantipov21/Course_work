from pprint import pprint
import sys
import json
sys.path.append('/usr/lib/python3/dist-packages')
import requests


def terminate(message, error_code):
    print(f'{message}. Error code {error_code}')
    exit(-1)
