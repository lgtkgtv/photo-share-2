#!/bin/bash
docker compose down --volumes --remove-orphans
docker ps -a | grep photo-sharing | awk '{print $1}' | xargs docker rm -f
docker images | grep photo-sharing | awk '{print $3}' | xargs docker rmi -f

