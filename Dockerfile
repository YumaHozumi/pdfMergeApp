FROM node:16.19.0-alpine

WORKDIR /app

RUN npm install -g http-server

COPY ./frontend/package*.json ./

RUN npm install \
&& mkdir dist

WORKDIR /app/dist

COPY ./frontend/dist/ .

EXPOSE 8080
CMD ["http-server", "-P", "http://backend:8080"]