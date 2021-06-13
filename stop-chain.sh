#!/bin/bash
echo "This may take a minute..."
docker stop $(docker ps -a -q)
docker rm $(docker ps -a -q)
