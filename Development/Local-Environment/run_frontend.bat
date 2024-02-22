@echo off

set DOCKERFILE_DIR= ../../Web-App/Frontend/

set IMAGE_TAG=frontend

set CONTAINER_NAME=frontend-container

docker build -t %IMAGE_TAG% %DOCKERFILE_DIR%

docker run --rm --name %CONTAINER_NAME% -p 80:80 %IMAGE_TAG%:latest