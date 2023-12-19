[![Run Tests](https://github.com/software-students-fall2023/5-final-project-plant5/actions/workflows/test.yml/badge.svg)](https://github.com/software-students-fall2023/5-final-project-plant5/actions/workflows/test.yml)
[![CI and CD](https://github.com/software-students-fall2023/5-final-project-plant5/actions/workflows/CI-CD.yml/badge.svg)](https://github.com/software-students-fall2023/5-final-project-plant5/actions/workflows/CI-CD.yml)

# MessageBoard
MessageBoard is a minimalist web app that allows for sharing text messages on a public message board.

## Team members
1. [Nathalia Xu](https://github.com/slurp-slurp)
2. [Robert (Bobby) Impastato](https://github.com/bobbyimpastato)
3. [Phoebus Yip](https://github.com/phoebusyip)
4. [Alicia Hwang](https://github.com/a-j-hwang)

## Links
Continuous delivery to Docker Hub: https://hub.docker.com/r/phoebusyip/plant5_message_board

Continuous deployment on DigitalOcean: http://159.65.244.47:5000/

## How to Run:
Clone the repository. 

In the root directory, run `docker-compose up --build`

Navigate to [localhost:5000](http://localhost:5000/) to access the web app.    

Please make sure that port 5000 (for the web app) and port 27017 (for mongodb) are available on your machine. If unavailable, visit the deployed site or manually change the ports to use the web app.