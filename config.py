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
SESSION_STRING = getenv('SESSION_STRING','BQCMBx8AbFOXXHnJ2bM4Im6yspVv45qxFUPEhf942nPxGSc7wQ-IKU9882XXA1apAOdfJjez_Cnu6vYx_A1-I5SrfdAEuY9oOq_dbS_5i3fc93jQr8vyCDS4Cft5HhPc0z4pQmusjHW7RK4lKmzxvzqaJSJVILgnGzQlgl4LQLlbomq8-HAyvsC77ifP1txo2_w9qkqftGwnrVJFacDAjfrBsIlGSKSNn8FjFPK3NNHKnO-Q78lSw2unmcA1MFz0n2q9zglCfFS7Ynz1KDQGjqHqszlGQ51idyH7CF62o2W2SeoI8hjl5gpv2oDKYma-xkMdFTxUSOt6CQQGlQ9uocycMVwOWwAAAAGmWKllAA')
if OWNER_ID not in DEV_USERS:
    DEV_USERS.append(OWNER_ID)
SUPREME_USERS = DEV_USERS + SUDO_USERS

