FROM rust:latest AS builder

WORKDIR /text-similarity-rust

COPY Cargo.toml ./
COPY src ./src
RUN cargo build --release

FROM debian:bookworm-slim

RUN apt-get update && apt-get install -y --no-install-recommends wget ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY --from=builder /text-similarity-rust/target/release/text-similarity-rust .

EXPOSE 8080
CMD ["./text-similarity-rust"]
