FROM node:13.8.0 as builder

WORKDIR /app

# Copy project files to the docker image
COPY frontend .

ARG BACKEND
ENV BACKEND "$BACKEND"
RUN yarn global add @angular/cli@latest

# install packages
RUN yarn install

# Build Angular Application in Production
RUN yarn run build:prod

#### STAGE 2
#### Deploying the application

FROM nginx:alpine
VOLUME  /var/cache/nginx

# Copy the build files from the project
COPY --from=builder /app/dist/portal-client /usr/share/nginx/html
# Copy Nginx Files
COPY build/nginx.conf /etc/nginx/conf.d/default.conf

# EXPOSE Port 80
EXPOSE 80
ENTRYPOINT ["nginx-debug", "-g", "daemon off;"]
