package main

import (
	"encoding/json"
	"log"
	"net/http"
	"os"

	"github.com/gin-gonic/gin"
)

type BlogPost struct {
	Title   string `json:"title"`
	Content string `json:"content"`
}

func main() {
	r := gin.Default()
	r.LoadHTMLGlob("templates/*")
	r.Static("/static", "./static")

	r.GET("/", func(c *gin.Context) {
		c.HTML(http.StatusOK, "index.html", gin.H{})
	})

	r.GET("/endpoint", func(c *gin.Context) {
		c.String(http.StatusOK, "We are so back!")
	})

	r.GET("/about", func(c *gin.Context) {
		c.HTML(http.StatusOK, "about.html", gin.H{})
	})

	r.GET("/landing", func(c *gin.Context) {
		file, err := os.ReadFile("posts.json")
		if err != nil {
			log.Fatalf("Unable to read the JSON file: %v", err)
		}

		var posts []BlogPost
		err = json.Unmarshal(file, &posts)
		if err != nil {
			log.Fatalf("Unable to unmarshal JSON: %v", err)
		}

		c.HTML(http.StatusOK, "landing.html", gin.H{
			"Posts": posts,
		})
	})

	r.Run()
}
