package config

import (
	// "log"
	"os"
)

type Config struct {
	ServerAddress string
}

func Load() (*Config, error) {
	serverAddress := os.Getenv("SERVER_ADDRESS")
	if serverAddress == "" {
		serverAddress = ":8080"
	}

	return &Config{
		ServerAddress: serverAddress,
	}, nil
}
