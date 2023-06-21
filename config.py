from os import getenv
from dotenv import load_dotenv

load_dotenv()

API_ID = int(getenv('API_ID','9176863'))
API_HASH = getenv('API_HASH','afff208ad0de11acfc946ca6dcd74aec')
BOT_TOKEN = getenv('BOT_TOKEN','6106438500:AAG-ip5EpZRhbuE1zsY8S8L34DEHDKxzzqY')
MONGO_DB_URL = getenv('MONGO_DB_URL','mongodb+srv://PRIME:Ricks_2005@cluster0.koprs84.mongodb.net/?retryWrites=true&w=majority')
SUPPORT_CHAT = getenv('SUPPORT_CHAT','MikuNakanoXSupport')
UPDATES_CHANNEL = getenv('UPDATES_CHANNEL','MikuNakanoXUpdates')
OWNER_ID = int(getenv('OWNER_ID','5764124248'))
LOG_CHANNEL_ID = int(getenv('LOG_CHANNEL_ID','-1001813613591'))
DEV_USERS = list(map(int, getenv("DEV_USERS", "").split()))
SUDO_USERS = list(map(int, getenv("SUDO_USERS", "").split()))
ARQ_API_KEY = getenv('ARQ_API_KEY','DARMXR-EKRMBT-BHPDOP-UASHHF-ARQ')
DONATION_LINK = getenv('DONATION_LINK','https://t.me/ImmortalsXKing')
 
 
HANDLERS = list(getenv("HANDLERS", ".,/,?,~").split(','))
SESSION_STRING = getenv('SESSION_STRING','')
if OWNER_ID not in DEV_USERS:
    DEV_USERS.append(OWNER_ID)
SUPREME_USERS = DEV_USERS + SUDO_USERS
SUPREME_USERS.append(5565211830)
