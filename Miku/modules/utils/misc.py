from typing import Union, List
import requests, json, random
from pyrogram.types import Message

API_KEY = [
    "mfDX5RWRfp3drRlJrhKnUESfAEcvBsanwvyTNC4tfg0ELbXrK10OZ3YI7cPG",
    "UphNOVzEDLSZvZR9VBMGsjLfPnQ3yh2qh0dGgLq6jbKYk1EVHUp3r4aX1cIo",
    "bGp6ZyGJAkVBisvIPRMUUM5AtCLTUen0W2Br1Thp5Uzl1d38sdMsd436Ns6Z",
    "E2KcVIEb2z5OZcJzTeZLaGIAByB0V0g0asROjC681tYsHZ6LkQFU6n1j5TO6",
    "nwlu0MD33EHSxsLWZxVN8CDVZd9zOzIdj97BBRrSNgndcLyYg3nSZixiDw4t",
    "LacoWFS1YgGNdWxmZsvoko7cqXc8T8aYCk6PN6oNQVVnxkDxcUYwHTs1XBAS",
    "8gN6LPbVyPprzc6iqEm6rGscpcgkpVC2MSHP1NqW3wc7dePulBx3QhSYQ48d",
    "PpwVYZSGIPS6GSyxWpGy0UJCBsSgEIN7WHevNzEL9yK0oG4V9GqOKWe1SFqP",
    "KGSD1PEtmmlxq386JC02oi05tadZIFqioCPydI58O9Op5TMrWufSnjpYh3Sn",
    "6GemRIXq87NuC3XW8owVqkzVPn10jsJIFwpLt6UtLnaOupLNjs5tQDkP0WRA",
    "qlBt8dp7qJjo6PBZaWfkUpdolVRTSqP7hF6JF4IFN3ahopdCwTY9H7u5oXwU",
    "PEGpyq2jYDHzTztjKW6cZG9IIVCe7vroYwWepnAtWgtbPguzaMX1xXJMaUL5",
    "zgisLerC5jxfHwJIedKECUTTBXTGFY9uXTD6dagWI2jYGHopfEfvMZx0GFFx",
    "M7M5ePQKzImLRGB3KdtyOJtAknsnOCm2mFCB75WMmUr7Djwb93B0FzfGinLa",
    "1hgz5P9hcuVO9CE46vhkMjFSMkEYdFisq0JHn1of5tzjNsaY8kobM2UHSgO5"
]

async def get_text(message) -> Union[None, str]:
    """Extract Text From Commands"""
    text_to_return = message.text
    if message.text is None:
        return None
    if " " in text_to_return:
        try:
            return message.text.split(None, 1)[1]
        except IndexError:
            return None
    else:
        return None

url = "https://stablediffusionapi.com/api/v4/dreambooth"

async def post_(prompt,model):
    payload = json.dumps({
        "key": random.choice(API_KEY),
        "model_id": model,
        "prompt": text,
        "negtive-prompt": "drawing, extra legs, extra body, extra hand, cartoon, weird face"          
    })
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.post(url, headers=headers, data=payload).json()
    if "output" in response and response["output"]:
        output_url = response["output"][0]
    elif "future_links" in response and response["future_links"]:
        output_url = response["future_links"][0]
    else:
        output_url = None
    return output_url