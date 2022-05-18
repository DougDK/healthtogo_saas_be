flask run

docker rm -vf $(docker ps -aq)
docker rmi -f $(docker images -aq)

aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 470778815705.dkr.ecr.us-east-1.amazonaws.com
docker build -t healthtogo .
docker tag healthtogo:latest 470778815705.dkr.ecr.us-east-1.amazonaws.com/healthtogo:latest
docker push 470778815705.dkr.ecr.us-east-1.amazonaws.com/healthtogo:latest