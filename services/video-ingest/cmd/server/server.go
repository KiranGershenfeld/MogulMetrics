package main

import (
	"context"
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"time"
	"video-ingest/internal/channels"
	channelDB "video-ingest/internal/channels/database"
	"video-ingest/internal/health"
	"video-ingest/internal/videos"
	videosDB "video-ingest/internal/videos/database"

	"video-ingest/internal/config"
	"video-ingest/internal/database"
	"video-ingest/internal/middleware"
	"video-ingest/pkg/logging"

	"github.com/gin-gonic/gin"
	"github.com/spf13/cobra"
	"go.uber.org/fx"
	"go.uber.org/fx/fxevent"
	"go.uber.org/zap"
	"go.uber.org/zap/zapcore"
)

var serverCmd = &cobra.Command{
	Use: "server",
	Run: func(cmd *cobra.Command, args []string) {
		runApplication()
	},
}

func runApplication() {
	// load configs and sets default logger configs.
	conf, err := config.Load(configFile)
	if err != nil {
		log.Fatal(err)
	}
	logging.SetConfig(&logging.Config{
		Encoding:    conf.LoggingConfig.Encoding,
		Level:       zapcore.Level(conf.LoggingConfig.Level),
		Development: conf.LoggingConfig.Development,
	})
	defer logging.DefaultLogger().Sync()

	// setup application(di + run server)
	app := fx.New(
		fx.Supply(conf),
		fx.Supply(logging.DefaultLogger().Desugar()),
		fx.WithLogger(func(log *zap.Logger) fxevent.Logger {
			return &fxevent.ZapLogger{Logger: log.Named("fx")}
		}),
		fx.StopTimeout(conf.ServerConfig.GracefulShutdown+time.Second),
		fx.Invoke(
			printAppInfo,
		),
		fx.Provide(
			health.NewHandler,

			// setup database
			database.NewDatabase,

			channelDB.NewChannelDB,
			channels.NewHandler,

			videosDB.NewVideoDB,
			videos.NewHandler,

			newServer,
		),
		fx.Invoke(
			videos.RouteV1,
			health.RouteV1,

			func(r *gin.Engine) {},
		),
	)
	app.Run()
}

func newServer(lc fx.Lifecycle, cfg *config.Config) *gin.Engine {
	gin.SetMode(gin.DebugMode)
	r := gin.New()
	r.Use(middleware.LoggingMiddleware("/metric"), gin.Recovery())

	srv := &http.Server{
		Addr:         fmt.Sprintf(":%d", cfg.ServerConfig.Port),
		Handler:      r,
		ReadTimeout:  cfg.ServerConfig.ReadTimeout,
		WriteTimeout: cfg.ServerConfig.WriteTimeout,
	}
	lc.Append(fx.Hook{
		OnStart: func(ctx context.Context) error {
			logging.FromContext(ctx).Infof("Start to rest api server :%d", cfg.ServerConfig.Port)
			go func() {
				if err := srv.ListenAndServe(); err != nil && err != http.ErrServerClosed {
					logging.DefaultLogger().Errorw("failed to close http server", "err", err)
				}
			}()
			return nil
		},
		OnStop: func(ctx context.Context) error {
			logging.FromContext(ctx).Info("Stopped rest api server")
			return srv.Shutdown(ctx)
		},
	})
	return r
}

func printAppInfo(cfg *config.Config) {
	b, _ := json.MarshalIndent(&cfg, "", "  ")
	logging.DefaultLogger().Infof("application information\n%s", string(b))
}
