@echo off

set DOCKERFILE_DIR= ../../Web-App/Backend/

set IMAGE_TAG=backend

set CONTAINER_NAME=backend-container

docker build -t %IMAGE_TAG% %DOCKERFILE_DIR%

docker run --rm --name %CONTAINER_NAME% -p 8080:5000 %IMAGE_TAG%:latest