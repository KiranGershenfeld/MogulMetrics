package model

import (
	"time"
)

type Video struct {
	YoutubeID    string    `gorm:"column:youtube_id;primaryKey;autoIncrement:false"`
	ChannelID    string    `gorm:"column:channel_id;primaryKey;autoIncrement:false"`
	Title        string    `gorm:"column:title"`
	ThumbnailUrl string    `gorm:"column:thumbnail_url"`
	UploadTime   time.Time `gorm:"column:upload_time"`
	CreatedAt    time.Time `gorm:"column:created_at"`
	DeletedAt    time.Time `gorm:"column:deleted_at"`
	UpdatedAt    time.Time `gorm:"column:updated_at"`
}
