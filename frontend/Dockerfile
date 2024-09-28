FROM node:16.19.0-alpine

WORKDIR /app

RUN npm install -g http-server

COPY ./package*.json ./

RUN npm install

COPY . .

RUN npm run build

WORKDIR /app/dist

EXPOSE 8080
CMD ["http-server", "-P", "http://backend:8080"]