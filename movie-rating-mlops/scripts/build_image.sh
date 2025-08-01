#!/bin/bash

# ==============================================
# Movie Rating MLOps - Docker Image Build Script
# 영화 평점 예측 MLOps 도커 이미지 빌드 스크립트
# ==============================================

set -e  # 에러 발생시 스크립트 종료

# 색상 정의 (터미널 출력용)
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 프로젝트 설정
PROJECT_NAME="movie-rating-mlops"
IMAGE_NAME="movie-rating-dev"
IMAGE_TAG="latest"

echo -e "${BLUE}===============================================${NC}"
echo -e "${BLUE}  Movie Rating MLOps - Docker Image Build${NC}"
echo -e "${BLUE}===============================================${NC}"

# 1. 현재 위치 확인
echo -e "\n${YELLOW}Step 1: 현재 디렉토리 확인${NC}"
if [ ! -f "Dockerfile" ]; then
    echo -e "${RED}오류: Dockerfile을 찾을 수 없습니다.${NC}"
    echo -e "${RED}프로젝트 루트 디렉토리에서 실행해주세요.${NC}"
    exit 1
fi

if [ ! -f "requirements.txt" ]; then
    echo -e "${RED}오류: requirements.txt를 찾을 수 없습니다.${NC}"
    exit 1
fi

echo -e "${GREEN}필수 파일들이 확인되었습니다.${NC}"

# 2. 기존 이미지 확인
echo -e "\n${YELLOW}Step 2: 기존 이미지 확인${NC}"
if docker image inspect ${IMAGE_NAME}:${IMAGE_TAG} >/dev/null 2>&1; then
    echo -e "${YELLOW}기존 이미지가 존재합니다: ${IMAGE_NAME}:${IMAGE_TAG}${NC}"
    read -p "기존 이미지를 덮어쓰시겠습니까? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${BLUE}빌드를 취소합니다.${NC}"
        exit 0
    fi
else
    echo -e "${GREEN}새로운 이미지를 빌드합니다.${NC}"
fi

# 3. Docker 이미지 빌드
echo -e "\n${YELLOW}Step 3: Docker 이미지 빌드 시작${NC}"
echo -e "${BLUE}이미지명: ${IMAGE_NAME}:${IMAGE_TAG}${NC}"
echo -e "${BLUE}베이스 이미지: python:3.11-bookworm${NC}"

# 빌드 시작 시간 기록
BUILD_START_TIME=$(date +%s)

# Docker 빌드 실행
docker build \
    --tag ${IMAGE_NAME}:${IMAGE_TAG} \
    --file Dockerfile \
    .

# 빌드 완료 시간 계산
BUILD_END_TIME=$(date +%s)
BUILD_DURATION=$((BUILD_END_TIME - BUILD_START_TIME))

# 4. 빌드 결과 확인
echo -e "\n${YELLOW}Step 4: 빌드 결과 확인${NC}"
if docker image inspect ${IMAGE_NAME}:${IMAGE_TAG} >/dev/null 2>&1; then
    # 이미지 정보 출력
    IMAGE_SIZE=$(docker image inspect ${IMAGE_NAME}:${IMAGE_TAG} --format='{{.Size}}' | awk '{printf "%.1f MB", $1/1024/1024}')
    IMAGE_ID=$(docker image inspect ${IMAGE_NAME}:${IMAGE_TAG} --format='{{.Id}}' | cut -c8-19)
    
    echo -e "${GREEN}Docker 이미지 빌드 성공!${NC}"
    echo -e "${GREEN}이미지 이름: ${IMAGE_NAME}:${IMAGE_TAG}${NC}"
    echo -e "${GREEN}이미지 ID: ${IMAGE_ID}${NC}"
    echo -e "${GREEN}이미지 크기: ${IMAGE_SIZE}${NC}"
    echo -e "${GREEN}빌드 시간: ${BUILD_DURATION}초${NC}"
else
    echo -e "${RED}Docker 이미지 빌드 실패${NC}"
    exit 1
fi

# 5. 다음 단계 안내
echo -e "\n${BLUE}===============================================${NC}"
echo -e "${BLUE}  빌드 완료! 다음 단계를 진행하세요${NC}"
echo -e "${BLUE}===============================================${NC}"
echo -e "${GREEN}환경 설정: ./scripts/setup_env.sh${NC}"
echo -e "${GREEN}컨테이너 실행: ./scripts/run_dev.sh${NC}"
echo -e "${GREEN}전체 가이드: ./scripts/quick_start.sh${NC}"