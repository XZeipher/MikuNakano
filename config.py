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
SESSION_STRING = getenv('SESSION_STRING','BQBaQFe1KpaU0oz4FB7JCm1C0uq9Tvd0tKXMqcXU2pyeWwL9J7fRzv86k2aJ70FGwi4CIVdrSwL2VhcxiUp4A5oPNIknPECWFR1rjhGEWQmtCaU4gBkeBGANp7JAC_Q5x36ygDJCKApYc5oae08r5bxw1uqsm3C6lS9-g_Xcurmf1s9GE7LZQylmuGq18NTK5F9ZqNfURijhE3M_DW0-ZH3kTZSbsTYUcfg00cokDt2prkm7guub1n_IyUtflTy4QPN3H5ZQKcdfEY-0akilJb-WTjeLvpZKAIYhUmwCrZssP6J-w1qGHhnG8QMrPxpPp03ctsnlC_zCT6YjiYqlWlJ8AAAAAWwBgnkA')
if OWNER_ID not in DEV_USERS:
    DEV_USERS.append(OWNER_ID)
SUPREME_USERS = DEV_USERS + SUDO_USERS

