// Lab 10: The Minimal Container -- given Go API (do not modify).
//
// Serves GET /healthz on :8080 with a JSON body containing the
// Success Token, so `docker run` + `curl` is enough to verify your
// containerization worked.
package main

import (
	"encoding/json"
	"log"
	"net/http"
)

func healthzHandler(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(map[string]string{
		"status": "ok",
		"token":  "CONTAINER_MINIMAL_OK",
	})
}

func main() {
	http.HandleFunc("/healthz", healthzHandler)
	log.Println("api-service listening on :8080")
	log.Fatal(http.ListenAndServe(":8080", nil))
}
