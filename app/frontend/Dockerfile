FROM nginxinc/nginx-unprivileged:1.31-alpine

COPY --chmod=644 default.conf.template /etc/nginx/templates/default.conf.template
COPY --chmod=644 src/ /usr/share/nginx/html/

EXPOSE 8080
