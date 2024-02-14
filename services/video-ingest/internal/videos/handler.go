package videos

import (
	"encoding/xml"
	"fmt"
	"io"
	"net/http"
	"video-ingest/internal/config"
	"video-ingest/internal/database"
	"video-ingest/internal/middleware"
	"video-ingest/internal/middleware/handler"
	"video-ingest/internal/utils"
	videoDB "video-ingest/internal/videos/database"
	"video-ingest/internal/videos/model"
	"video-ingest/pkg/logging"

	"github.com/gin-gonic/gin"
)

func NewHandler(videoDB videoDB.VideoDB) *Handler {
	return &Handler{
		videoDB: videoDB,
	}
}

type Handler struct {
	videoDB videoDB.VideoDB
}

func (h *Handler) addVideo(c *gin.Context) {
	handler.HandleRequest(c, func(c *gin.Context) *handler.Response {
		logger := logging.FromContext(c)

		body, err := io.ReadAll(c.Request.Body)
		if err != nil {
			logger.Infof("Could not read request body")
			return nil
		}
		logger.Infof("Request body: %v", string(body))

		var feed Feed
		if err := xml.Unmarshal(body, &feed); err != nil {
			logger.Errorf("Could not unmarshal xml to feed: %v", err)
			return handler.NewErrorResponse(http.StatusBadRequest, handler.InvalidBodyValue, "could not parse video feed xml", err)
		}
		// if err := c.ShouldBind(&feed); err != nil {
		// 	logger.Errorw("channel.handler.register failed to bind", "err", err)
		// 	var details []*validate.ValidationErrDetail
		// 	if vErrs, ok := err.(validator.ValidationErrors); ok {
		// 		details = validate.ValidationErrorDetails(&feed.Title, "json", vErrs)
		// 	}
		// 	logger.Infof("Could not parse video feed xml: %v", details)
		// 	return handler.NewErrorResponse(http.StatusBadRequest, handler.InvalidBodyValue, "could not parse video feed xml", details)
		// }

		logger.Infof("feed: %v", feed)

		uploadTime, err := utils.ParseTime(feed.Entry.Published)
		if err != nil {
			logger.Infof("Could not parse timestamp %v. err: %v", feed.Entry.Published, err)
			return handler.NewErrorResponse(http.StatusBadRequest, handler.InvalidBodyValue, fmt.Sprintf("could not parse video feed timestamp. Expected RFC3339 but got %s", feed.Entry.Published), nil)
		}

		video := model.Video{
			YoutubeID:  feed.Entry.YoutubeID,
			ChannelID:  feed.Entry.ChannelID,
			Title:      feed.Entry.Title,
			UploadTime: *uploadTime,
		}

		err = h.videoDB.AddVideo(c.Request.Context(), &video)
		if err != nil {
			if database.IsKeyConflictErr(err) {
				return handler.NewErrorResponse(http.StatusConflict, handler.DuplicateEntry, "duplicate article title", nil)
			}
			return handler.NewInternalErrorResponse(err)
		}
		return handler.NewSuccessResponse(http.StatusCreated, NewVideoResponse(&video))
	})
}

func (h *Handler) verifySubscription(c *gin.Context) {
	// logger := logging.FromContext(c)
	// Parse query parameters
	mode := c.Query("hub.mode")
	topic := c.Query("hub.topic")
	challenge := c.Query("hub.challenge")

	// Validate required parameters
	if mode == "" || topic == "" || challenge == "" {
		c.Error(fmt.Errorf("mode, topic, or challenge missing from hub subscription verification request"))
	}

	// Simulate a successful verification response
	c.Header("Content-Type", "text/plain")
	c.String(http.StatusOK, "%s", challenge)
}

func RouteV1(cfg *config.Config, h *Handler, r *gin.Engine) {
	v1 := r.Group("v1/api")
	v1.Use(middleware.RequestIDMiddleware(), middleware.TimeoutMiddleware(cfg.ServerConfig.WriteTimeout))

	videoV1 := v1.Group("videos")
	// anonymous
	videoV1.Use()
	{
		videoV1.POST("/feed", h.addVideo)
		videoV1.GET("/feed", h.verifySubscription)
	}
}

type Feed struct {
	XMLName xml.Name `xml:"feed"`
	Link    []Link   `xml:"link"`
	Title   string   `xml:"title"`
	Updated string   `xml:"updated"`
	Entry   Entry    `xml:"entry"`
}

type Link struct {
	Rel  string `xml:"rel,attr"`
	Href string `xml:"href,attr"`
}

type Entry struct {
	ID        string `xml:"id"`
	YoutubeID string `xml:"videoId"`
	ChannelID string `xml:"channelId"`
	Title     string `xml:"title"`
	Link      Link   `xml:"link"`
	Author    Author `xml:"author"`
	Published string `xml:"published"`
	Updated   string `xml:"updated"`
}

type Author struct {
	Name string `xml:"name"`
	URI  string `xml:"uri"`
}
