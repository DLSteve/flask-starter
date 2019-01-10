#!/usr/bin/env bash

BUILD_BASE=false
PUSH=false
DEPLOY=false
RELEASE_VERSION=false
BASE_NAME="iamdockerdev.azurecr.io/iam/base/azure-python"
WEB_NAME="iamdockerdev.azurecr.io/iam/web/flask-starter-web"
TASK_NAME="iamdockerdev.azurecr.io/iam/web/flask-starter-task"

while [[ $# -gt 0 ]]
do
KEY="$1"

case ${KEY} in
    -b|--build-base-image)
    BUILD_BASE=true
    shift # past argument
    ;;
    -i|--base-image-version)
    BASE_VER="$2"
    shift # past argument
    shift # past value
    ;;
    -p|--push-images)
    PUSH=true
    shift # past argument
    ;;
    -v|--version)
    APP_VER="$2"
    shift # past argument
    shift # past value
    ;;
    -d|--deploy-images)
    DEPLOY=true
    shift # past argument
    ;;
    -r|--release)
    RELEASE_VERSION=true
    shift # past argument
    ;;
    *)    # unknown option
    shift # past argument
    ;;
esac
done

echo "Building images."
if ! [ ${APP_VER} ] ; then
    APP_VER=$(grep -o "version='[^']*'" ./setup.py | sed -e "s/'//g" -e "s/version=//g")
fi

if [ "$BUILD_BASE" = true ] ; then
    if ! [ ${BASE_VER} ] ; then
        echo "No base image version provided."
        exit
    fi
    docker build -f ./docker/azure-python/Dockerfile -t ${BASE_NAME}:latest -t ${BASE_NAME}:${BASE_VER} .
fi

COMMIT=$(git log --pretty=format:'%h' -n 1)
COMMIT_FULL=$(git rev-parse HEAD)
rm ./configs/version
touch ./configs/version
echo "${APP_VER}" >> ./configs/version
echo "${COMMIT}" >> ./configs/version
echo "${COMMIT_FULL}" >> ./configs/version

docker build -f ./docker/flask-starter-web/Dockerfile -t ${WEB_NAME}:latest -t ${WEB_NAME}:${APP_VER} -t ${WEB_NAME}:${COMMIT} .
docker build -f ./docker/flask-starter-task/Dockerfile -t ${TASK_NAME}:latest -t ${TASK_NAME}:${APP_VER} -t ${TASK_NAME}:${COMMIT} .

echo "Cleaning old images."
docker rm -v $(docker ps --filter status=exited -q 2>/dev/null) 2>/dev/null
docker rmi $(docker images --filter dangling=true -q 2>/dev/null) 2>/dev/null
docker rmi $(docker images | grep "${WEB_NAME}" | awk 'NR>3 {print $3}') 2>/dev/null
docker rmi $(docker images | grep "${TASK_NAME}" | awk 'NR>3 {print $3}') 2>/dev/null


if [ "$PUSH" = true ] ; then
    echo "Uploading to registry."
    if [ "$BUILD_BASE" = true ] ; then
        docker push ${BASE_NAME}:latest
        docker push ${BASE_NAME}:${BASE_VER}
    fi

    docker push ${WEB_NAME}:latest
    docker push ${TASK_NAME}:latest

    if [ "$RELEASE_VERSION" = true ] ; then
        docker push ${WEB_NAME}:${APP_VER}
        docker push ${TASK_NAME}:${APP_VER}
    else
        docker push ${WEB_NAME}:${COMMIT}
        docker push ${TASK_NAME}:${COMMIT}
    fi


    if [ "$DEPLOY" = true ] ; then
        echo "Deploying Task image."
        if [ "$RELEASE_VERSION" = true ] ; then
            kubectl set image deployment/flask-starter-task flask-starter-task=${TASK_NAME}:${APP_VER}
        else
            kubectl set image deployment/flask-starter-task flask-starter-task=${TASK_NAME}:${COMMIT}
        fi
        sleep 10
        echo "Deploying Web image."
        if [ "$RELEASE_VERSION" = true ] ; then
            kubectl set image deployment/flask-starter-web flask-starter-web=${WEB_NAME}:${APP_VER}
        else
            kubectl set image deployment/flask-starter-web flask-starter-web=${WEB_NAME}:${COMMIT}
        fi
    fi
fi