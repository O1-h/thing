FROM golang:1.26-alpine AS build
WORKDIR /src
COPY go.mod ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 go build -o /app .
FROM scratch
COPY --from=build /app /app
USER 65532:65532
EXPOSE 8081
ENTRYPOINT ["/app"]
