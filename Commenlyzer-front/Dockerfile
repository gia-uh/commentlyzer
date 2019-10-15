# build stage
FROM node:lts-alpine as build-stage
WORKDIR /app
COPY Commenlyzer-front/package*.json ./
#RUN npm install && mkdir /node_modules && cp -r node_modules /node_modules
#RUN cp -ru node_modules /usr/local/lib
RUN npm install
COPY Commenlyzer-front .
RUN npm run build
# ENTRYPOINT ['npm', 'install']
CMD ["npm", "run", "serve"]
EXPOSE 8000