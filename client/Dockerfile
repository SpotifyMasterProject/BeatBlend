FROM node:20-alpine AS builder
WORKDIR /app

COPY package*.json ./
RUN npm install --ignore-scripts

COPY . .

EXPOSE 8080

CMD npm run dev