from dotenv import load_dotenv
import os
load_dotenv()


def get_env(key: str , default_value = None) -> str:
    return os.getenv(key,default_value)

def get_env_int(key: str , default_value = None) -> int:
    return int(os.getenv(key,default_value))