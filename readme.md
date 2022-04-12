# PreviaMe!

v0.1



# Deploy



    git pull
    docker build -t PreviaMe .
    docker run -d --name PreviaMe-Container -p 8000:8000 PreviaMe
