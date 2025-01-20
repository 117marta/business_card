from base64 import b64encode
from io import BytesIO

from qrcode import make


def generate_qr(data="tst"):
    buffer = BytesIO()
    qr = make(data, box_size=10)
    qr.save(buffer)
    buffer.seek(0)
    img = b64encode(buffer.read()).decode()
    return f"data:image/png;base64,{img}"
