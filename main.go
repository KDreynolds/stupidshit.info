package main

import (
	"bytes"
	"encoding/json"
	"html/template"
	"io"
	"log"
	"net/http"
	"os"
	"time"

	"github.com/gin-gonic/gin"
)

func formatDate(t time.Time) string {
	// Format the date as "January 2, 2006"
	return t.Format("January 2, 2006")
}

type BlogPost struct {
	Title   string    `json:"title"`
	Content string    `json:"content"`
	Date    time.Time `json:"date"`
}

type FormData struct {
	Name    string `json:"name"`
	Email   string `json:"email"`
	Message string `json:"message"`
}

func main() {
	r := gin.Default()
	// r.LoadHTMLGlob("templates/*") // Remove this line
	r.Static("/static", "./static")

	r.Use(func(c *gin.Context) {
		if c.Request.Header.Get("X-Forwarded-Proto") != "https" {
			secureUrl := "https://" + c.Request.Host + c.Request.RequestURI
			c.Redirect(http.StatusPermanentRedirect, secureUrl)
			c.Abort()
		} else {
			c.Next()
		}
	})

	funcMap := template.FuncMap{
		"dateFormat": formatDate,
	}
	templ := template.Must(template.New("").Funcs(funcMap).ParseGlob("templates/*"))
	r.SetHTMLTemplate(templ)

	r.GET("/", func(c *gin.Context) {
		c.HTML(http.StatusOK, "index.html", gin.H{})
	})

	r.GET("/endpoint", func(c *gin.Context) {
		c.String(http.StatusOK, "We are so back!")
	})

	r.GET("/about", func(c *gin.Context) {
		c.HTML(http.StatusOK, "about.html", gin.H{})
	})

	r.GET("/contact", func(c *gin.Context) {
		c.HTML(http.StatusOK, "contact.html", nil) // Assuming you have a contact.html template
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

	r.POST("/send-email", func(c *gin.Context) {
		// Parse URL-encoded form data directly without trying to read and unmarshal JSON
		if err := c.Request.ParseForm(); err != nil {
			log.Printf("ParseForm() error: %v", err)
			c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid form data"})
			return
		}

		// Access form values directly
		name := c.Request.FormValue("name")
		email := c.Request.FormValue("email")
		message := c.Request.FormValue("message")

		// Assuming you want to continue using the FormData struct for internal handling
		formData := FormData{
			Name:    name,
			Email:   email,
			Message: message,
		}

		// Log formData to verify correct parsing (optional, for debugging purposes)
		log.Printf("Received form data: %+v", formData)

		// Prepare the data to send to Nocodeapi or any other internal processing
		data := [][]string{
			{formData.Name, formData.Email, formData.Message},
		}

		// Convert the data to JSON for the Nocodeapi request
		jsonData, err := json.Marshal(data)
		if err != nil {
			log.Printf("Error marshalling data: %v", err)
			c.JSON(http.StatusInternalServerError, gin.H{"error": "Error preparing data"})
			return
		}

		// Set up the request to Nocodeapi
		url := "https://v1.nocodeapi.com/kdreynolds/google_sheets/QEpNwsnHlEBZIPDQ?tabId=Sheet1"
		req, err := http.NewRequest("POST", url, bytes.NewBuffer(jsonData))
		if err != nil {
			log.Printf("Error creating request: %v", err)
			c.JSON(http.StatusInternalServerError, gin.H{"error": "Error sending data"})
			return
		}
		req.Header.Set("Content-Type", "application/json")

		// Perform the request
		client := &http.Client{}
		resp, err := client.Do(req)
		if err != nil {
			log.Printf("Error sending request to Nocodeapi: %v", err)
			c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to send data"})
			return
		}
		defer resp.Body.Close()

		// Read the response
		body, err := io.ReadAll(resp.Body)
		if err != nil {
			log.Printf("Error reading response: %v", err)
			c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to read response"})
			return
		}

		// Unmarshal the JSON response
		var result map[string]interface{}
		if err := json.Unmarshal(body, &result); err != nil {
			log.Printf("Error unmarshalling response: %v", err)
			c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to process response"})
			return
		}

		// Respond with the result
		c.JSON(http.StatusOK, result)
	})

	r.Run()
}
