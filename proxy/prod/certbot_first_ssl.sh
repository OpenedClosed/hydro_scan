#!/bin/sh

certbot certonly --webroot --webroot-path=/certbot --register-unsafely-without-email --agree-tos -d $DOMAIN
echo "if error exist certs - continue work"
