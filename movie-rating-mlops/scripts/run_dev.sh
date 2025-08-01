#!/bin/bash

# ==============================================
# Movie Rating MLOps - Development Container Runner
# 영화 평점 예측 MLOps 개발 컨테이너 실행 스크립트
# ==============================================

set -e  # 에러 발생시 스크립트 종료

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 설정값
IMAGE_NAME="movie-rating-dev"
IMAGE_TAG="latest"
CONTAINER_NAME="movie-rating-dev-container"
HOST_PORT_API=8000
HOST_PORT_API_ALT=8001
CONTAINER_PORT_API=8000
CONTAINER_PORT_API_ALT=8001

echo -e "${BLUE}===============================================${NC}"
echo -e "${BLUE}  Movie Rating MLOps - Development Container${NC}"
echo -e "${BLUE}===============================================${NC}"

# 1. Docker 이미지 존재 확인
echo -e "\n${YELLOW}Step 1: Docker 이미지 확인${NC}"
if ! docker image inspect ${IMAGE_NAME}:${IMAGE_TAG} >/dev/null 2>&1; then
    echo -e "${RED}Docker 이미지를 찾을 수 없습니다: ${IMAGE_NAME}:${IMAGE_TAG}${NC}"
    echo -e "${YELLOW}먼저 이미지를 빌드해주세요: ./scripts/build_image.sh${NC}"
    exit 1
fi
echo -e "${GREEN}Docker 이미지 확인 완료${NC}"

# 2. 환경변수 파일 확인
echo -e "\n${YELLOW}Step 2: 환경설정 파일 확인${NC}"
if [ ! -f ".env" ]; then
    echo -e "${RED}.env 파일을 찾을 수 없습니다.${NC}"
    echo -e "${YELLOW}먼저 환경설정을 완료해주세요: ./scripts/setup_env.sh${NC}"
    exit 1
fi
echo -e "${GREEN}환경설정 파일 확인 완료${NC}"

# 3. 기존 컨테이너 확인 및 정리
echo -e "\n${YELLOW}Step 3: 기존 컨테이너 확인${NC}"
if docker container inspect ${CONTAINER_NAME} >/dev/null 2>&1; then
    echo -e "${YELLOW}기존 컨테이너가 존재합니다: ${CONTAINER_NAME}${NC}"
    
    # 컨테이너 상태 확인
    CONTAINER_STATUS=$(docker container inspect ${CONTAINER_NAME} --format='{{.State.Status}}')
    echo -e "${BLUE}컨테이너 상태: ${CONTAINER_STATUS}${NC}"
    
    if [ "$CONTAINER_STATUS" = "running" ]; then
        echo -e "${YELLOW}실행 중인 컨테이너를 중지합니다...${NC}"
        docker stop ${CONTAINER_NAME}
    fi
    
    echo -e "${YELLOW}기존 컨테이너를 제거합니다...${NC}"
    docker rm ${CONTAINER_NAME}
fi

# 4. 포트 사용 확인
echo -e "\n${YELLOW}Step 4: 포트 사용 확인${NC}"
check_port() {
    local port=$1
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1; then
        echo -e "${YELLOW}포트 $port가 이미 사용 중입니다.${NC}"
        return 1
    else
        echo -e "${GREEN}포트 $port 사용 가능${NC}"
        return 0
    fi
}

# 메인 포트 확인
if check_port $HOST_PORT_API; then
    USE_PORT=$HOST_PORT_API
elif check_port $HOST_PORT_API_ALT; then
    echo -e "${BLUE}대체 포트 ${HOST_PORT_API_ALT}을 사용합니다.${NC}"
    USE_PORT=$HOST_PORT_API_ALT
else
    echo -e "${RED}사용 가능한 포트가 없습니다. (${HOST_PORT_API}, ${HOST_PORT_API_ALT})${NC}"
    exit 1
fi

# 5. 개발 컨테이너 실행
echo -e "\n${YELLOW}Step 5: 개발 컨테이너 실행${NC}"
echo -e "${BLUE}컨테이너명: ${CONTAINER_NAME}${NC}"
echo -e "${BLUE}포트 매핑: ${USE_PORT}:8000${NC}"
echo -e "${BLUE}볼륨 마운트: $(pwd) → /workspace${NC}"

# Docker run 명령 실행
docker run -itd \
    --name ${CONTAINER_NAME} \
    --env-file .env \
    -p ${USE_PORT}:8000 \
    -p ${HOST_PORT_API_ALT}:8001 \
    -v "$(pwd)":/workspace \
    -w /workspace \
    ${IMAGE_NAME}:${IMAGE_TAG}

# 6. 실행 결과 확인
echo -e "\n${YELLOW}Step 6: 컨테이너 실행 확인${NC}"
sleep 2  # 컨테이너 시작 대기

if docker container inspect ${CONTAINER_NAME} --format='{{.State.Status}}' | grep -q "running"; then
    CONTAINER_ID=$(docker container inspect ${CONTAINER_NAME} --format='{{.Id}}' | cut -c1-12)
    echo -e "${GREEN}개발 컨테이너가 성공적으로 실행되었습니다!${NC}"
    echo -e "${GREEN}컨테이너 ID: ${CONTAINER_ID}${NC}"
    echo -e "${GREEN}API 서버 포트: http://localhost:${USE_PORT}${NC}"
else
    echo -e "${RED}컨테이너 실행에 실패했습니다.${NC}"
    docker logs ${CONTAINER_NAME}
    exit 1
fi

# 7. 사용법 안내
echo -e "\n${BLUE}===============================================${NC}"
echo -e "${BLUE}  컨테이너 실행 완료! 사용법 안내${NC}"
echo -e "${BLUE}===============================================${NC}"
echo -e "${GREEN}컨테이너 접속:${NC}"
echo -e "   docker exec -it ${CONTAINER_NAME} bash"
echo -e ""
echo -e "${GREEN}실습 명령어 예시:${NC}"
echo -e "   docker exec -it ${CONTAINER_NAME} python src/main.py preprocessing --date 250101"
echo -e "   docker exec -it ${CONTAINER_NAME} python src/main.py train --model_name movie_predictor"
echo -e "   docker exec -it ${CONTAINER_NAME} python src/main.py inference --data '[1,123,4508,7.5,1204.7]'"
echo -e ""
echo -e "${GREEN}컨테이너 중지:${NC}"
echo -e "   docker stop ${CONTAINER_NAME}"
echo -e ""
echo -e "${GREEN}컨테이너 로그 확인:${NC}"
echo -e "   docker logs ${CONTAINER_NAME}"