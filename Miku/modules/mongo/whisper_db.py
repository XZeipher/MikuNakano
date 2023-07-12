import threading
from Miku import db

collection = db.whisper
INSERTION_LOCK = threading.RLock()

class Whispers:
    @staticmethod
    async def add_whisper(WhisperId, WhisperData):
        with INSERTION_LOCK:
            whisper = {
                'WhisperId': WhisperId,
                'whisperData': WhisperData
            }
            await collection.insert_one(whisper)

    @staticmethod
    async def del_whisper(WhisperId):
        with INSERTION_LOCK:
            await collection.delete_one({'WhisperId': WhisperId})

    @staticmethod
    async def get_whisper(WhisperId):
        whisper = await collection.find_one({'WhisperId': WhisperId})
        if whisper:
            return whisper['whisperData']
        return None
