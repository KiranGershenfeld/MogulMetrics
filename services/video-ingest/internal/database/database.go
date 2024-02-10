package database

import (
	"fmt"
	"time"
	"video-ingest/internal/config"
	"video-ingest/pkg/logging"

	"go.uber.org/zap/zapcore"
	"gorm.io/driver/postgres"
	"gorm.io/gorm"
)

// NewDatabase creates a new database with given config
func NewDatabase(cfg *config.Config) (*gorm.DB, error) {
	var (
		db     *gorm.DB
		err    error
		logger = NewLogger(time.Second, true, zapcore.Level(cfg.DBConfig.LogLevel))
	)

	dsn := fmt.Sprintf("host=%s user=%s password=%s dbname=%s port=%s sslmode=%s TimeZone=US/Pacific",
		cfg.DBConfig.Credentials.Host, cfg.DBConfig.Credentials.Username, cfg.DBConfig.Credentials.Password, cfg.DBConfig.Credentials.Name, cfg.DBConfig.Credentials.Port, cfg.DBConfig.Credentials.SSLMode)

	for i := 0; i <= 30; i++ {
		db, err = gorm.Open(postgres.Open(dsn), &gorm.Config{Logger: logger})
		if err == nil {
			break
		}
		logging.DefaultLogger().Warnf("failed to open database: %v", err)
		time.Sleep(500 * time.Millisecond)
	}
	if err != nil {
		return nil, err
	}

	rawDB, err := db.DB()
	if err != nil {
		return nil, err
	}
	rawDB.SetMaxOpenConns(cfg.DBConfig.Pool.MaxOpen)
	rawDB.SetMaxIdleConns(cfg.DBConfig.Pool.MaxIdle)
	rawDB.SetConnMaxLifetime(cfg.DBConfig.Pool.MaxLifetime)

	if cfg.DBConfig.Migrate.Enable {
		err := migrateDB(dsn, cfg.DBConfig.Migrate.Dir)
		if err != nil {
			return nil, err
		}
	}
	return db, nil
}
