package database

import (
	"context"
	"video-ingest/internal/database"
	"video-ingest/internal/videos/model"
	"video-ingest/pkg/logging"

	"gorm.io/gorm"
)

type VideoDB interface {
	// SaveArticle saves a given article with tags.
	// if not exist tags, then save a new tag
	AddVideo(ctx context.Context, channel *model.Video) error
}

// NewArticleDB creates a new article db with given db
func NewVideoDB(db *gorm.DB) VideoDB {
	return &videoDB{db: db}

}

type videoDB struct {
	db *gorm.DB
}

func (c *videoDB) AddVideo(ctx context.Context, video *model.Video) error {
	logger := logging.FromContext(ctx)
	db := database.FromContext(ctx, c.db)

	if err := db.WithContext(ctx).Create(video).Error; err != nil {
		logger.Errorw("video.db.AddVideo failed to save video", "err", err)
		if database.IsKeyConflictErr(err) {
			return database.ErrKeyConflict
		}
		return err
	}
	return nil
}
