from os import getenv
from dotenv import load_dotenv

load_dotenv()

API_ID = int(getenv('API_ID','18770647'))
API_HASH = getenv('API_HASH','ed11b8af8b51418dbac60b456d1429a7')
BOT_TOKEN = getenv('BOT_TOKEN','5429814096:AAETs76j16YmrF50d-HLEbjJRVG2HSuH4Tg')
MONGO_DB_URL = getenv('MONGO_DB_URL','mongodb+srv://PRIME:Ricks_2005@cluster0.koprs84.mongodb.net/?retryWrites=true&w=majority')
SUPPORT_CHAT = getenv('SUPPORT_CHAT','MikuNakanoXSupport')
UPDATES_CHANNEL = getenv('UPDATES_CHANNEL','MikuNakanoXUpdates')
OWNER_ID = int(getenv('OWNER_ID','6393014348'))
LOG_CHANNEL_ID = int(getenv('LOG_CHANNEL_ID','-1001805033582'))
DEV_USERS = list(map(int, getenv("DEV_USERS", "5565211830").split()))
SUDO_USERS = list(map(int, getenv("SUDO_USERS", "1811267624").split()))
ARQ_API_KEY = getenv('ARQ_API_KEY','DARMXR-EKRMBT-BHPDOP-UASHHF-ARQ')
DONATION_LINK = getenv('DONATION_LINK','https://t.me/ImmortalsXKing')
 
 
HANDLERS = list(getenv("HANDLERS", ".,/,?,~").split(','))
SESSION_STRING = getenv('SESSION_STRING','BQB9HzneGpGjgiWapXfmoH9Y1fgJcmwWILjbOO5gzazdxup9EaA3b8tY7nwZ17B6ogg-g8L8CgmDfgAuqz584Odw5zRCV3Zh-YZOdEbtB3uCs_iLQ1JJGZ4NQ05kehLj0OAIQvOmIN-I8sf1iqy-YpPd359RIu2KhWc9aKWyGYtwSnhW4glAzEIU0IAd2uPmsrv4Vj0IHj5alXAhxEuVt9vY2ve09iNBOyhiNjcl4B-l5lNbym8OHohRKg_67B30rwm3NWiIjXsZe7BMbepFUur4tamXF9jBLuNzKcMpWElPydHck4kcSneBpD52Y5KcjgfOCqG2gkBbQD6f_l-Wiw1MAAAAAX0NqEwA')
if OWNER_ID not in DEV_USERS:
    DEV_USERS.append(OWNER_ID)
SUPREME_USERS = DEV_USERS + SUDO_USERS

