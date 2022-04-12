# PreviaMe!

v0.1



# Deploy



    git pull
    docker stop previame-container
    docker rm previame-container
    docker rmi previame
    docker build -t previame .
    docker run -d --name previame-container -p 8000:8000 previame
