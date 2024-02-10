package config

import (
	"time"
)

var defaultConfig = map[string]interface{}{
	"server.host":             "localhost",
	"server.port":             8080,
	"server.readTimeout":      "5s",
	"server.writeTimeout":     "10s",
	"server.gracefulShutdown": "30s",

	"logging.level":       -1,
	"logging.encoding":    "console",
	"logging.development": true,

	"jwt.secret":      "secret-key",
	"jwt.sessionTime": "864000s",

	"db.credentials.username": "postgres",
	"db.credentials.password": "",
	"db.credentials.host":     "db",
	"db.credentials.port":     "5432",
	"db.credentials.name":     "local-trending",
	"db.credentials.sslmode":  "disable",
	"db.logLevel":             1,
	"db.migrate.enable":       false,
	"db.migrate.dir":          "",
	"db.pool.maxOpen":         10,
	"db.pool.maxIdle":         5,
	"db.pool.maxLifetime":     "5m",

	"cache.enabled":            false,
	"cache.prefix":             "article-",
	"cache.type":               "redis",
	"cache.ttl":                60 * time.Second,
	"cache.redis.cluster":      false,
	"cache.redis.endpoints":    []string{"localhost:6379"},
	"cache.redis.readTimeout":  "3s",
	"cache.redis.writeTimeout": "3s",
	"cache.redis.dialTimeout":  "5s",
	"cache.redis.poolSize":     10,
	"cache.redis.poolTimeout":  "1m",
	"cache.redis.maxConnAge":   "0",
	"cache.redis.idleTimeout":  "5m",

	"metrics.namespace": "article_server",
	"metrics.subsystem": "",
}
