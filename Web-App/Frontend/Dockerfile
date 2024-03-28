# Stage 1: Build Stage
FROM node:latest as build

ARG ANGULAR_ENVIRONMENT=production

WORKDIR /usr/local/app

COPY package*.json ./

RUN npm install

COPY . .

RUN npm run build -- --configuration=${ANGULAR_ENVIRONMENT}

# Stage 2: Production Stage
FROM nginx:latest

RUN rm -rf /usr/share/nginx/html/*

COPY --from=build /usr/local/app/dist/frontend/browser /usr/share/nginx/html

EXPOSE 80
