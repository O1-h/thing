package main

import (
	"testing"
	"time"
)

func TestBucketBurst(t *testing.T) {
	b := newTokenBucket(2, 0)
	if !b.allow() || !b.allow() || b.allow() {
		t.Fatal("burst limit not enforced")
	}
}
func TestBucketRefill(t *testing.T) {
	b := newTokenBucket(1, 10)
	b.allow()
	b.lastRefill = time.Now().Add(-time.Second)
	if !b.allow() {
		t.Fatal("tokens did not refill")
	}
}
func TestLimiterIsolation(t *testing.T) {
	rl := newRateLimiter()
	for i := 0; i < 40; i++ {
		if !rl.allow("a") {
			t.Fatal("early rejection")
		}
	}
	if rl.allow("a") {
		t.Fatal("burst not bounded")
	}
	if !rl.allow("b") {
		t.Fatal("clients share bucket")
	}
}
