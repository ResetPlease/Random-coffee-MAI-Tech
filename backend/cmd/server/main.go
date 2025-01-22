package main

import (
	"coffee/internal/api"
	"coffee/internal/config"
	"log"
	"net/http"

	"github.com/gorilla/mux"
)

func main() {
	cfg, err := config.Load()
	if err != nil {
		log.Fatalf("Failed to load config: %v", err)
	}

	router := mux.NewRouter()

	api.RegisterRoutes(router)

	log.Printf("Starting server on %s...\n", cfg.ServerAddress)
	if err := http.ListenAndServe(cfg.ServerAddress, router); err != nil {
		log.Fatalf("Failed to start server: %v", err)
	}
}
