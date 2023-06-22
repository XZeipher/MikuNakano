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
        "prompt": prompt,
        "negative_prompt": "((out of frame)), ((extra fingers)), mutated hands, ((poorly drawn hands)), ((poorly drawn face)), (((mutation))), (((deformed))), (((tiling))), ((naked)), ((tile)), ((fleshpile)), ((ugly)), (((abstract))), blurry, ((bad anatomy)), ((bad proportions)), ((extra limbs)), cloned face, glitchy, ((extra breasts)), ((double torso)), ((extra arms)), ((extra hands)), ((mangled fingers)), ((missing breasts)), (missing lips), ((ugly face)), ((fat)), (worst quality, low quality:1.4), monochrome, zombie, (interlocked fingers), disfigured, kitsch, ugly, oversaturated, grain, low-res, Deformed, blurry, bad anatomy, disfigured, poorly drawn face, mutation, mutated, extra limb, ugly, poorly drawn hands, missing limb, blurry, floating limbs, disconnected limbs, malformed hands, blur, out of focus, long neck, long body, disgusting, poorly drawn, childish, mutilated, mangled, old, surreal, calligraphy, sign, writing, watermark, text, body out of frame, extra legs, extra arms, extra feet, poorly drawn feet, cross-eye, blurry, bad anatomy",
        "width": "1024",
        "height": "1024",
        "samples": "1",
        "num_inference_steps": "30",
        "seed": random.randint(1,574165781454),
        "self_attention":"yes",
        "guidance_scale": 7.5,
        "webhook": "None",
        "track_id": "None"
        })
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.post(url, headers=headers, data=payload)
    data = response.json()
    if 'status' in data:
    	while data['status'] == 'processing':
            time.sleep(5)
            response = requests.get(data['fetch_result'])
            data = response.json()
        if 'output' in data and len(data['output']) > 0:
        	output_url =  data['output'][0]
        elif 'future_links' in data and len(data['future_links']) > 0:
        	output_url = data['future_links'][0]
        else:
        	output_url = None
        return output_url
            