FROM nginx:stable-alpine

COPY nginx/nginx.proxy.conf /etc/nginx/nginx.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]