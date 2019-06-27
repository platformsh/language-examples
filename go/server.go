package main

import (
	"github.com/gin-gonic/gin"
	_ "github.com/go-sql-driver/mysql"
	Config "github.com/platformsh/language-examples/conf"
	mysql "github.com/platformsh/language-examples/examples"
	"net/http"
)

func setupRouter() *gin.Engine {

	r := gin.Default()

	// Hello World
	r.GET("/mysql", func(c *gin.Context) {
		out := mysql.MySQL()
		c.String(http.StatusOK, out)
	})

	return r
}

func main() {

	r := setupRouter()

	// Listen and Server in the port defined by Platform.sh.
	r.Run(":" + Config.PshConfig.Port())
}
