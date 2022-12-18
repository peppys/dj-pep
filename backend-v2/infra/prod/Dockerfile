FROM golang:1.16.4 as builder
WORKDIR /opt/app

# Copy code from host and compile
COPY go.mod .
COPY go.sum .
RUN go mod download

COPY cmd ./cmd
COPY gen ./gen
COPY internal ./internal
COPY static ./static

RUN go build -o /bin/api cmd/api.go

# Copy binary to debian and run
FROM debian:jessie-slim
WORKDIR /opt/app

# Need ca-certificates to make https requests from container
RUN apt-get update
RUN apt-get install -y ca-certificates

COPY --from=builder /bin/api ./api
COPY --from=builder /opt/app/static ./static

# Start API
ENTRYPOINT ./api
