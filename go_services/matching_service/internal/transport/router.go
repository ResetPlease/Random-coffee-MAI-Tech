package transport

import (
	"matching/internal/transport/handlers"
	"matching/internal/transport/middlewares"

	"github.com/gin-gonic/gin"
)

func SetupRouting() *gin.Engine {
	r := gin.Default()

	public := r.Group("/public")
	public.Use(middlewares.AuthorizationMiddleware())
	public.GET("/", handlers.HelloHandler)

	return r
}
