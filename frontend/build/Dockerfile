FROM node:14.11-stretch as builder

COPY . /usr/src/app/
WORKDIR /usr/src/app
RUN yarn install
RUN yarn build

EXPOSE 3000
ENV NUXT_HOST=0.0.0.0
ENV NUXT_PORT=3000
ENTRYPOINT [ "yarn", "start" ]
