To run:
docker-compose -f tests/docker-compose.test.yml up --build

at web-app directory, run: 
docker build -t mypytestcontainer -f tests/Dockerfile.test .
docker run mypytestcontainer

