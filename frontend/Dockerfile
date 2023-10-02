FROM node:lts-alpine3.18 as base

WORKDIR /app

COPY package*.json .
COPY yarn.lock .

RUN yarn

FROM base as prod
COPY . .
RUN yarn quasar build
