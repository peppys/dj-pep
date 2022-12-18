package config

import (
	"os"
)

type DBConfig struct {
	User string
	Pass string
	Host string
	Port string
	Name string
}

type AuthConfig struct {
	AccessTokenSigningKey string
}

type AppConfig struct {
	DB   DBConfig
	Auth AuthConfig
}

func NewAppConfig() *AppConfig {
	return &AppConfig{
		DB: DBConfig{
			User: getEnv("DB_USER", "dbuser"),
			Pass: getEnv("DB_PASS", "dbpass"),
			Host: getEnv("DB_HOST", "127.0.0.1"),
			Port: getEnv("DB_PORT", "3306"),
			Name: getEnv("DB_NAME", "dbname"),
		},
		Auth: AuthConfig{
			AccessTokenSigningKey: getEnv("ACCESS_TOKEN_SIGNING_KEY", "some-key"),
		},
	}
}

func getEnv(key string, defaultVal string) string {
	if value, exists := os.LookupEnv(key); exists {
		return value
	}

	return defaultVal
}
