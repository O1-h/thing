// Route /work to the worker and limit requests from each client IP.
package main

import (
	"encoding/json"
	"io"
	"log"
	"math"
	"net"
	"net/http"
	"os"
	"sync"
	"time"
)

// tokenBucket is a simple per-client rate limiter: `capacity` tokens,
// refilling at `refillPerSecond`, one token consumed per request.
type tokenBucket struct {
	mu              sync.Mutex
	tokens          float64
	capacity        float64
	refillPerSecond float64
	lastRefill      time.Time
}

func newTokenBucket(capacity, refillPerSecond float64) *tokenBucket {
	return &tokenBucket{
		tokens:          capacity,
		capacity:        capacity,
		refillPerSecond: refillPerSecond,
		lastRefill:      time.Now(),
	}
}

func (b *tokenBucket) allow() bool {
	b.mu.Lock()
	defer b.mu.Unlock()
	now := time.Now()
	elapsed := now.Sub(b.lastRefill).Seconds()
	b.tokens = math.Min(b.capacity, b.tokens+elapsed*b.refillPerSecond)
	b.lastRefill = now
	if b.tokens >= 1.0 {
		b.tokens -= 1.0
		return true
	}
	return false
}

type rateLimiter struct {
	mu      sync.Mutex
	buckets map[string]*tokenBucket
}

func newRateLimiter() *rateLimiter {
	return &rateLimiter{buckets: make(map[string]*tokenBucket)}
}

func (rl *rateLimiter) allow(clientKey string) bool {
	rl.mu.Lock()
	b, ok := rl.buckets[clientKey]
	if !ok {
		// Allow a burst of 40, then refill at 20 requests per second.
		// Explain any changes to these values in your README.
		b = newTokenBucket(40, 20)
		rl.buckets[clientKey] = b
	}
	rl.mu.Unlock()
	return b.allow()
}

func main() {
	workerURL := os.Getenv("WORKER_URL")
	if workerURL == "" {
		workerURL = "http://worker-service"
	}

	limiter := newRateLimiter()
	client := &http.Client{Timeout: 10 * time.Second}

	http.HandleFunc("/healthz", func(w http.ResponseWriter, r *http.Request) {
		json.NewEncoder(w).Encode(map[string]string{"status": "ok"})
	})

	http.HandleFunc("/work", func(w http.ResponseWriter, r *http.Request) {
		clientKey, _, splitErr := net.SplitHostPort(r.RemoteAddr)
		if splitErr != nil {
			clientKey = r.RemoteAddr
		}
		if !limiter.allow(clientKey) {
			w.WriteHeader(http.StatusTooManyRequests)
			json.NewEncoder(w).Encode(map[string]string{"error": "rate limit exceeded"})
			return
		}

		resp, err := client.Get(workerURL + "/work")
		if err != nil {
			w.WriteHeader(http.StatusBadGateway)
			json.NewEncoder(w).Encode(map[string]string{"error": err.Error()})
			return
		}
		defer resp.Body.Close()

		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(resp.StatusCode)
		io.Copy(w, resp.Body)
	})

	log.Println("gateway listening on :8080")
	log.Fatal(http.ListenAndServe(":8080", nil))
}
