from os import getenv
from dotenv import load_dotenv

load_dotenv()

API_ID = int(getenv('API_ID','18770647'))
API_HASH = getenv('API_HASH','ed11b8af8b51418dbac60b456d1429a7')
BOT_TOKEN = getenv('BOT_TOKEN','8170552584:AAHCQuazy0jl-g4h9yZ82bJh_nCcaDLSfyk')
MONGO_DB_URL = getenv('MONGO_DB_URL','mongodb+srv://alphaxcoders:6D4IK0e4d4nOxapE@cluster0.lkpqx.mongodb.net/?retryWrites=true&w=majority')
SUPPORT_CHAT = getenv('SUPPORT_CHAT','MikuAlphaSupport')
UPDATES_CHANNEL = getenv('UPDATES_CHANNEL','kurumierrorlog')
OWNER_ID = int(getenv('OWNER_ID','7788597504'))
LOG_CHANNEL_ID = int(getenv('LOG_CHANNEL_ID','-1002269731879'))
DEV_USERS = list(map(int, getenv("DEV_USERS", "").split()))
SUDO_USERS = list(map(int, getenv("SUDO_USERS", "7535454753").split()))
ARQ_API_KEY = getenv('ARQ_API_KEY','DARMXR-EKRMBT-BHPDOP-UASHHF-ARQ')
DONATION_LINK = getenv('DONATION_LINK','https://t.me/CielSeraph')
 
 
HANDLERS = list(getenv("HANDLERS", ".,/,?,~").split(','))
SESSION_STRING = getenv('SESSION_STRING','BQCMBx8Asxkhwb9nJypqsn5Qd1mgag1k3yf0Qq8KpbxlPD15xjUYy_2BY5rrY56unk7qg8dRzjQpJ8hWD_vGoFMw9CiDagApBrgql-bM-R6zD69r4d_qU9T6dPT9dM5UqAEgaG8DDjwGG6lKG0BFBZSBevq3jVhxKapWYQcKAdnbDPQEQUsPylh0zAQayQHSZmI3-bL1A_9ugym6OxqUqTZ5yly_yZxTMeAmo0Fi93Md_r_1wS1LnPclaINgMB74jk4P2AY5-8R9pQHO6aSmu3K5Rprc1VvC7GlWSUnyWDHSjQz1bce3dW8D89VW_1ePtAyiNWdKDiQZJzbqivb2CV-i99Un-wAAAAGL2AqaAA')
if OWNER_ID not in DEV_USERS:
    DEV_USERS.append(OWNER_ID)
SUPREME_USERS = DEV_USERS + SUDO_USERS

