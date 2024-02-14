package channels

import "video-ingest/internal/channels/model"

type ChannelResponse struct {
	ID string `json:"id"`
}

// NewArticleResponse converts article model to ArticleResponse
func NewChannelResponse(a *model.Channel) *ChannelResponse {
	return &ChannelResponse{
		ID: a.YoutubeID,
	}
}
