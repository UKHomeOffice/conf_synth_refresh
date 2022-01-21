#!/usr/bin/env bash

docker build -t synth_data .
docker run synth_data 

container_id=$(docker ps -a | awk -F'[[:space:]][[:space:]]+' '{print $1,$2}' | awk '{ if($2=="synth_data") print $1}')

docker commit $container_id quay.io/ukhomeofficedigital/conf-synth-refresh
docker push quay.io/ukhomeofficedigital/conf-synth-refresh

docker rm $container_id

docker rmi synth_data