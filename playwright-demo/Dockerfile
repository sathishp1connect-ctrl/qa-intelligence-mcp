FROM mcr.microsoft.com/playwright:v1.55.0-jammy

WORKDIR /app

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Etc/UTC

RUN apt-get update && \
    apt-get install -y awscli tzdata && \
    rm -rf /var/lib/apt/lists/*

COPY package*.json ./
RUN npm ci

COPY . .

RUN mkdir -p reports

CMD ["npx", "playwright", "test"]