docker stop python-docker
docker rm python-docker
docker build --tag python-docker .
docker run -d -p 5000:5000 --name python-docker --restart unless-stopped -v $(pwd)/:/python-docker python-docker

