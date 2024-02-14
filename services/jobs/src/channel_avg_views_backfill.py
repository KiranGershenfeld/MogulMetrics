
from youtube import YouTubeAPI
import os
from sqlalchemy import text, exc, create_engine

youtube = YouTubeAPI(os.environ.get("YOUTUBE_API_KEY"))

def get_all_channels(engine):
    with engine.connect() as conn:
        records = conn.execute(text("SELECT youtube_id FROM channels"))
        conn.commit()
    
    return [record[0] for record in records]


def db_conn():
    username = os.environ.get("DB_CREDENTIALS_USERNAME")
    password = os.environ.get("DB_CREDENTIALS_PASSWORD")
    host = os.environ.get("DB_CREDENTIALS_HOST")
    port = os.environ.get("DB_CREDENTIALS_PORT")
    name = os.environ.get("DB_CREDENTIALS_NAME")

    DATABASE_URL = f'postgresql://{username}:{password}@{host}:{port}/{name}'
    print(DATABASE_URL)
    engine = create_engine(DATABASE_URL)

    return engine

if __name__ == "__main__":
    load_dotenv()

    engine = db_conn()
    channels = get_all_channels(engine)

    for channel in channels: 
        