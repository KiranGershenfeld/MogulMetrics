CREATE TABLE IF NOT EXISTS channels (
  youtube_id VARCHAR(255) PRIMARY KEY NOT NULL,
  name VARCHAR(512) NOT NULL,
  subscribers INTEGER,
  ingestion_active BOOLEAN,
  created_at TIMESTAMP,
  updated_at TIMESTAMP,
  deleted_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS videos (
  youtube_id VARCHAR(255) NOT NULL,
  channel_id VARCHAR(255),
  title VARCHAR(2048),
  thumbnail_url VARCHAR(2048),
  upload_time TIMESTAMP,
  created_at TIMESTAMP,
  updated_at TIMESTAMP,
  deleted_at TIMESTAMP,
  PRIMARY KEY (channel_id, youtube_id)
);