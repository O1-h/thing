package main

import (
	"encoding/json"
	"log"
	"net/http"
	"os"
	"strconv"
	"time"
)

// The health endpoint lets Docker and Kubernetes check this API.
func healthHandler(response http.ResponseWriter, request *http.Request) {
	response.Header().Set("Content-Type", "application/json")
	result := map[string]string{
		"status":   "ok",
		"instance": os.Getenv("HOSTNAME"),
		"token":    "APP_READY",
	}
	json.NewEncoder(response).Encode(result)
}

func main() {
	// Wait before opening the port so we can observe startup readiness.
	delayText := os.Getenv("STARTUP_DELAY_SECONDS")
	delaySeconds, _ := strconv.Atoi(delayText)
	time.Sleep(time.Duration(delaySeconds) * time.Second)

	// Register the endpoint, then listen for requests on port 8080.
	http.HandleFunc("/healthz", healthHandler)
	log.Fatal(http.ListenAndServe(":8080", nil))
}
