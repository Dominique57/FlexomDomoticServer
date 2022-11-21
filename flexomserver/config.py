from dotenv import load_dotenv
import os


load_dotenv()


class FlexomServerConfig:
    SECRET_KEY: str = os.environ.get("SECRET_KEY")
    VAPID_DIR: str = os.environ.get("VAPID_DIR")
    VAPID_CLAIM_EMAIL: str = os.environ.get("VAPID_CLAIM_EMAIL")
    SQLITE_PATH: str = os.environ.get("SQLITE_PATH")
