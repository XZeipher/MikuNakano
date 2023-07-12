import threading
from Miku import db

collection = db.whisper
INSERTION_LOCK = threading.RLock()

class Whispers:
    @staticmethod
    def add_whisper(WhisperId, WhisperData):
        with INSERTION_LOCK:
            whisper = {
                'WhisperId': WhisperId,
                'whisperData': WhisperData
            }
            collection.insert_one(whisper)

    @staticmethod
    def del_whisper(WhisperId):
        with INSERTION_LOCK:
            collection.delete_one({'WhisperId': WhisperId})

    @staticmethod
    def get_whisper(WhisperId):
        whisper = collection.find_one({'WhisperId': WhisperId})
        if whisper:
            return whisper['whisperData']
        return None

