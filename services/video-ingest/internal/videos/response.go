package videos

import "video-ingest/internal/videos/model"

type VideoResponse struct {
	ID string `json:"id"`
}

// NewArticleResponse converts article model to ArticleResponse
func NewVideoResponse(a *model.Video) *VideoResponse {
	return &VideoResponse{
		ID: a.YoutubeID,
	}
}
