import pickle

import rsa
from django.conf import settings


def sign_data(data):
    return rsa.sign(pickle.dumps(data), settings.PRIVATE_KEY, 'SHA-1')
