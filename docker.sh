CONTAINER_NAME="web_crawler"
CONTAINER_PORT="5000"

docker stop $CONTAINER_NAME
docker rm $CONTAINER_NAME
docker build --tag $CONTAINER_NAME .
docker run -d -p 5000:$CONTAINER_PORT --name $CONTAINER_NAME --restart unless-stopped -v $(pwd)/:/$CONTAINER_NAME $CONTAINER_NAME

