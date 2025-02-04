package main

import (
	"matching/internal/transport"
)

func main() {
	routerEngine := transport.SetupRouting()
	routerEngine.Run(":3000")
}
