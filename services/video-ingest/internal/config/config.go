package config

import (
	"encoding/json"
	"log"
	"path/filepath"
	"regexp"
	"strings"
	"time"

	"github.com/jeremywohl/flatten"
	"github.com/knadh/koanf"
	"github.com/knadh/koanf/parsers/yaml"
	"github.com/knadh/koanf/providers/confmap"
	"github.com/knadh/koanf/providers/env"
	"github.com/knadh/koanf/providers/file"
)

type Config struct {
	ServerConfig  ServerConfig  `json:"server"`
	LoggingConfig LoggingConfig `json:"logging" yaml:"logging"`
	DBConfig      DBConfig      `json:"db"`
}

type ServerConfig struct {
	Host             string        `json:"host"`
	Port             int           `json:"port"`
	ReadTimeout      time.Duration `json:"readTimeout"`
	WriteTimeout     time.Duration `json:"writeTimeout"`
	GracefulShutdown time.Duration `json:"gracefulShutdown"`
}

type LoggingConfig struct {
	Level       int    `json:"level"`
	Encoding    string `json:"encoding"`
	Development bool   `json:"development"`
}

type DBConfig struct {
	Credentials struct {
		Username string `json:"username"`
		Password string `json:"password"`
		Host     string `json:"host"`
		Port     string `json:"port"`
		Name     string `json:"name"`
		SSLMode  string `json:"sslmode"`
	} `json:"credentials"`
	LogLevel int `json:"logLevel"`
	Migrate  struct {
		Enable bool   `json:"enable"`
		Dir    string `json:"dir"`
	} `json:"migrate"`
	Pool struct {
		MaxOpen     int           `json:"maxOpen"`
		MaxIdle     int           `json:"maxIdle"`
		MaxLifetime time.Duration `json:"maxLifetime"`
	} `json:"pool"`
}

func Load(configPath string) (*Config, error) {
	k := koanf.New(".")

	// load from default config
	err := k.Load(confmap.Provider(defaultConfig, "."), nil)
	if err != nil {
		log.Printf("failed to load default config. err: %v", err)
		return nil, err
	}

	// load from env
	err = k.Load(env.Provider("", ".", func(s string) string {
		return strings.Replace(strings.ToLower(
			strings.TrimPrefix(s, "")), "_", ".", -1)
	}), nil)
	if err != nil {
		log.Printf("failed to load config from env. err: %v", err)
	}

	// load from config file if exist
	if configPath != "" {
		path, err := filepath.Abs(configPath)
		if err != nil {
			log.Printf("failed to get absoulute config path. configPath:%s, err: %v", configPath, err)
			return nil, err
		}
		log.Printf("load config file from %s", path)
		if err := k.Load(file.Provider(path), yaml.Parser()); err != nil {
			log.Printf("failed to load config from file. err: %v", err)
			return nil, err
		}
	}

	var cfg Config
	if err := k.UnmarshalWithConf("", &cfg, koanf.UnmarshalConf{Tag: "json", FlatPaths: false}); err != nil {
		log.Printf("failed to unmarshal with conf. err: %v", err)
		return nil, err
	}
	return &cfg, err
}

func (c *Config) MarshalJSON() ([]byte, error) {
	type conf Config
	alias := conf(*c)

	data, err := json.Marshal(&alias)
	if err != nil {
		return nil, err
	}

	flat, err := flatten.FlattenString(string(data), "", flatten.DotStyle)
	if err != nil {
		return nil, err
	}

	var m map[string]interface{}
	err = json.Unmarshal([]byte(flat), &m)
	if err != nil {
		return nil, err
	}

	maskKeys := map[string]struct{}{
		// add keys if u want to mask some properties.
		"jwt.secret": {},
	}

	for key, val := range m {
		if v, ok := val.(string); ok {
			m[key] = maskPassword(v)
		}
		if _, ok := maskKeys[key]; ok {
			switch v := val.(type) {
			case string:
				if v != "" {
					m[key] = "****"
				}
			default:
				m[key] = "****"
			}
		}
	}
	return json.Marshal(&m)
}

func maskPassword(val string) string {
	if val == "" {
		return ""
	}
	regex := regexp.MustCompile(`^(?P<protocol>.+?//)?(?P<username>.+?):(?P<password>.+?)@(?P<address>.+)$`)
	if !regex.MatchString(val) {
		return val
	}
	matches := regex.FindStringSubmatch(val)
	for i, v := range regex.SubexpNames() {
		if "password" == v {
			val = strings.ReplaceAll(val, matches[i], "****")
		}
	}
	return val
}
