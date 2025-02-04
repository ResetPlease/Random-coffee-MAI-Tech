package middlewares

import (
	"log"

	"github.com/gin-gonic/gin"
)

func AuthorizationMiddleware() gin.HandlerFunc {
	return func(c *gin.Context) {
		token := c.Request.Header.Get("Authorization")
		log.Println("Authorization token: ", token)
		c.Next()
	}
}
