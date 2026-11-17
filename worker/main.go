// Project 3: Scaler Cluster -- worker service (given, complete).
// Serves GET /work, doing a deliberately CPU-bound computation so the
// HPA has something real to scale on, and GET /healthz for probes.
package main

import (
	"encoding/json"
	"log"
	"math"
	"net/http"
)

func cpuBoundWork() float64 {
	total := 0.0
	for i := 0; i < 2_000_000; i++ {
		total += math.Sqrt(float64(i)) * math.Sin(float64(i))
	}
	return total
}

func workHandler(w http.ResponseWriter, r *http.Request) {
	result := cpuBoundWork()
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(map[string]interface{}{"result": result})
}

func healthzHandler(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(map[string]string{"status": "ok"})
}

func main() {
	http.HandleFunc("/work", workHandler)
	http.HandleFunc("/healthz", healthzHandler)
	log.Println("worker listening on :8081")
	log.Fatal(http.ListenAndServe(":8081", nil))
}
