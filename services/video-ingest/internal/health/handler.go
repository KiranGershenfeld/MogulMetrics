package health

import (
	"net/http"
	"video-ingest/internal/config"
	"video-ingest/internal/middleware"
	"video-ingest/internal/middleware/handler"
	videoDB "video-ingest/internal/videos/database"

	"github.com/gin-gonic/gin"
)

func NewHandler(videoDB videoDB.VideoDB) *Handler {
	return &Handler{}
}

type Handler struct {
}

func (h *Handler) health(c *gin.Context) {
	handler.HandleRequest(c, func(c *gin.Context) *handler.Response {
		return handler.NewSuccessResponse(http.StatusOK, "healthy")
	})
}

func RouteV1(cfg *config.Config, h *Handler, r *gin.Engine) {
	v1 := r.Group("")
	v1.Use(middleware.TimeoutMiddleware(cfg.ServerConfig.WriteTimeout))
	v1.GET("/health", h.health)
}
