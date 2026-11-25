FROM node:22-slim

RUN apt-get update && apt-get install -y --no-install-recommends wget \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY package.json ./
RUN npm install

COPY src ./src

EXPOSE 8080

# WEB_CONCURRENCY = number of Node cluster workers (one per core recommended),
# since a single Node process runs JS on one thread.
ENV WEB_CONCURRENCY=1
CMD ["npx", "tsx", "src/index.ts"]
