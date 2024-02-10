package channels

import (
	"context"
	"errors"
	"fmt"
	"net/http"
	"net/url"
	channelDB "video-ingest/internal/channels/database"
	"video-ingest/internal/channels/model"
	"video-ingest/internal/config"
	"video-ingest/internal/database"
)

func NewHandler(cfg *config.Config, channelDB channelDB.ChannelDB) *Handler {
	return &Handler{
		config:    cfg,
		channelDB: channelDB,
	}
}

type Handler struct {
	config    *config.Config
	channelDB channelDB.ChannelDB
}

func (h *Handler) AddChannel(channelID string, channelName string, subscribe bool, subscriberCount int) {
	// logger := logging.FromContext(cmd.Context())
	// bind
	channel := model.Channel{
		YoutubeID:       channelID,
		Name:            channelName,
		Subscribers:     subscriberCount,
		IngestionActive: subscribe,
	}

	if subscribe {
		SubscribeToChannel(h.config, channel.YoutubeID)
	}

	err := h.channelDB.AddChannel(context.Background(), &channel)
	if err != nil {
		if database.IsKeyConflictErr(err) {
			fmt.Printf("\n Duplicate channel entry %s", channelID)
			return
		}
		fmt.Printf("\n Unhandled error adding channel %s", channelID)
		return
	}
	fmt.Printf("\n Successfully added channel %s", channelID)
	return

}

func SubscribeToChannel(cfg *config.Config, channelID string) (err error) {
	// Prepare post data
	postData := url.Values{
		"hub.callback":      {fmt.Sprintf("http://%s/v1/api/videos/feed", cfg.ServerConfig.Host)},
		"hub.mode":          {"subscribe"},
		"hub.topic":         {fmt.Sprintf("https://www.youtube.com/xml/feeds/videos.xml?channel_id=%s", channelID)},
		"hub.lease_seconds": {"864000"},
	}

	// Create HTTP client
	client := &http.Client{}

	// Make POST request
	res, err := client.PostForm("https://pubsubhubbub.appspot.com/", postData)
	if err != nil {
		return err
	}
	defer res.Body.Close()

	// Check response status
	if res.StatusCode == http.StatusAccepted {
		fmt.Println("Subscription successful!")
		return nil
	} else {
		fmt.Println("Subscription failed. Status:", res.Status)
		return errors.New("subscription failed")
	}
}
