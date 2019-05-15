import hashlib

class HashMaker:

    # hashes a given text using MD5
    @staticmethod
    def md5_hash_from_text(text):
        return hashlib.md5(text).hexdigest()
