# Use an official Python runtime as a parent image
FROM nginx:alpine
# Set work directory
WORKDIR /

RUN rm -rf /usr/share/nginx/html/*

COPY src/templates/nginx.conf /etc/nginx/nginx.conf
COPY src/templates/*.html /usr/share/nginx/html/

VOLUME /usr/share/nginx/html/

EXPOSE 80
ENTRYPOINT ["nginx", "-g", "daemon off;"]
