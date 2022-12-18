FROM golang:1.16.4 as builder
WORKDIR /opt/app

# Copy code from host and compile
COPY go.mod .
COPY go.sum .
RUN go mod download

COPY cmd ./cmd
COPY gen ./gen
COPY internal ./internal

ENTRYPOINT go run cmd/api.go
