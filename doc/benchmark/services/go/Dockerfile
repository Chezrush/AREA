FROM golang:1.23-alpine AS builder

WORKDIR /app

COPY go.mod ./
COPY main.go ./
RUN go mod tidy
RUN CGO_ENABLED=0 GOOS=linux go build -o /out/app main.go

FROM alpine

RUN apk add --no-cache wget
WORKDIR /out
COPY --from=builder /out/app /out/app

EXPOSE 8080
CMD ["./app"]
