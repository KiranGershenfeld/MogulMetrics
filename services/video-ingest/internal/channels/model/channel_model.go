package model

import (
	"time"
)

type Channel struct {
	YoutubeID       string    `gorm:"column:youtube_id;primaryKey;autoIncrement:false"`
	Name            string    `gorm:"column:name"`
	Subscribers     int       `gorm:"column:subscribers"`
	IngestionActive bool      `gorm:"column:ingestion_active"`
	CreatedAt       time.Time `gorm:"column:created_at"`
	DeletedAt       time.Time `gorm:"column:deleted_at"`
	UpdatedAt       time.Time `gorm:"column:updated_at"`
}
