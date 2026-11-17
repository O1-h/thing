# Lab 10: The Minimal Container -- starter.
#
# Complete the TODOs below. See the assignment,
# Part B, for the full requirements.

# ---- Builder stage ----
FROM golang:1.22-alpine AS builder
WORKDIR /app

# TODO (Requirement 1): copy go.mod FIRST (and go.sum if present) and run `go mod
# download` before copying the rest of the source -- this is the fix
# for the cache-invalidation bug from Part A, Question 2. This app
# has no external dependencies (go.mod has no `require` lines), so
# `go mod download` is a no-op here, but do it in the right order
# anyway -- that ordering is exactly what's being graded.
COPY api-service/go.mod ./
# TODO: RUN go mod download

COPY api-service/ .
# TODO: RUN CGO_ENABLED=0 go build -o main .

# ---- Final stage ----
# TODO (Requirement 2): FROM scratch (or alpine:3.19 if you want a
# shell for debugging -- justify your choice in the theory doc, tied
# to Part A, Question 4). Copy only the compiled `main` binary (and
# ca-certificates if you go the scratch route and ever need outbound
# TLS, which this specific app doesn't). EXPOSE 8080 and
# ENTRYPOINT ["/main"].
