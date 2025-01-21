from base64 import b64encode
from io import BytesIO

import requests
from django.conf import settings
from qrcode import make

from rae.exceptions import CeremeoException


def generate_qr(data="tst"):
    buffer = BytesIO()
    qr = make(data, box_size=10)
    qr.save(buffer)
    buffer.seek(0)
    img = b64encode(buffer.read()).decode()
    return f"data:image/png;base64,{img}"


def send_data_to_ceremeo(payload, url, method="POST"):
    """
    Make an API call to the Ceremeo URL with the provided data.
    """
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Token {settings.CEREMEO_API_KEY}",
    }

    try:
        response = requests.request(method=method, url=url, json=payload, headers=headers, timeout=20)
    except Exception as e:
        raise CeremeoException(e)

    return response.json()
