# Dockerfile-nginx
FROM nginx:alpine
# Nginx will listen on this port
EXPOSE 80
# Remove the default config file that
# /etc/nginx/nginx.conf includes
RUN rm /etc/nginx/conf.d/default.conf
# We copy the requirements file in order to install
# Python dependencies
COPY webapp.conf /etc/nginx/conf.d/
COPY html/ /usr/share/nginx/html