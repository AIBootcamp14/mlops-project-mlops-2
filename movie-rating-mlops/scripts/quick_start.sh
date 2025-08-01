#!/bin/bash

# ==============================================
# Movie Rating MLOps - Quick Start Script
# 영화 평점 예측 MLOps 원클릭 시작 스크립트
# ==============================================

set -e  # 에러 발생시 스크립트 종료

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

echo -e "${PURPLE}===============================================${NC}"
echo -e "${PURPLE}   Movie Rating MLOps - Quick Start${NC}"
echo -e "${PURPLE}===============================================${NC}"
echo -e "${BLUE}영화 평점 예측 MLOps 프로젝트를 빠르게 시작합니다!${NC}"
echo -e ""

# 프로젝트 정보 표시
echo -e "${YELLOW}프로젝트 정보:${NC}"
echo -e "   • TMDB API 기반 영화 데이터 수집"
echo -e "   • PyTorch를 활용한 평점 예측 모델"  
echo -e "   • FastAPI 기반 서비스 배포"
echo -e "   • Docker 컨테이너 환경"
echo -e ""

# 시작 확인
echo -e "${YELLOW}자동 설정을 시작하시겠습니까?${NC}"
echo -e "${BLUE} (환경설정 → 이미지빌드 → 컨테이너실행 순서로 진행됩니다)${NC}"
read -p "계속하시겠습니까? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${BLUE}설정을 취소합니다.${NC}"
    echo -e "${YELLOW}개별 스크립트를 사용하여 단계별로 진행할 수 있습니다:${NC}"
    echo -e "   ./scripts/setup_env.sh      # 환경 설정"
    echo -e "   ./scripts/build_image.sh    # 이미지 빌드"
    echo -e "   ./scripts/run_dev.sh        # 컨테이너 실행"
    exit 0
fi

# 전체 실행 시간 측정 시작
TOTAL_START_TIME=$(date +%s)

echo -e "\n${PURPLE}===============================================${NC}"
echo -e "${PURPLE}  1️⃣  환경 설정 (Environment Setup)${NC}"
echo -e "${PURPLE}===============================================${NC}"

# Step 1: 환경 설정
if [ -f "scripts/setup_env.sh" ]; then
    chmod +x scripts/setup_env.sh
    ./scripts/setup_env.sh
else
    echo -e "${RED}setup_env.sh 스크립트를 찾을 수 없습니다.${NC}"
    exit 1
fi

echo -e "\n${PURPLE}===============================================${NC}"
echo -e "${PURPLE}  2️⃣  Docker 이미지 빌드 (Image Build)${NC}"
echo -e "${PURPLE}===============================================${NC}"

# Step 2: 이미지 빌드
if [ -f "scripts/build_image.sh" ]; then
    chmod +x scripts/build_image.sh
    ./scripts/build_image.sh
else
    echo -e "${RED}build_image.sh 스크립트를 찾을 수 없습니다.${NC}"
    exit 1
fi

echo -e "\n${PURPLE}===============================================${NC}"
echo -e "${PURPLE}  3️⃣  개발 컨테이너 실행 (Container Run)${NC}"
echo -e "${PURPLE}===============================================${NC}"

# Step 3: 컨테이너 실행
if [ -f "scripts/run_dev.sh" ]; then
    chmod +x scripts/run_dev.sh
    ./scripts/run_dev.sh
else
    echo -e "${RED}run_dev.sh 스크립트를 찾을 수 없습니다.${NC}"
    exit 1
fi

# 전체 실행 시간 계산
TOTAL_END_TIME=$(date +%s)
TOTAL_DURATION=$((TOTAL_END_TIME - TOTAL_START_TIME))

# 최종 완료 메시지
echo -e "\n${PURPLE}===============================================${NC}"
echo -e "${PURPLE}  Movie Rating MLOps 설정 완료!${NC}"
echo -e "${PURPLE}===============================================${NC}"
echo -e "${GREEN}총 소요 시간: ${TOTAL_DURATION}초${NC}"
echo -e "${GREEN}개발 환경이 준비되었습니다!${NC}"
echo -e ""

# 다음 단계 안내
echo -e "${YELLOW}지금 바로 시작하기:${NC}"
echo -e ""
echo -e "${BLUE}1️⃣  컨테이너에 접속:${NC}"
echo -e "   docker exec -it movie-rating-dev-container bash"
echo -e ""
echo -e "${BLUE}2️⃣  데이터 수집 테스트:${NC}"
echo -e "   docker exec -it movie-rating-dev-container python src/main.py preprocessing --date 250101"
echo -e ""
echo -e "${BLUE}3️⃣  모델 학습 테스트:${NC}"
echo -e "   docker exec -it movie-rating-dev-container python src/main.py train --model_name movie_predictor"
echo -e ""
echo -e "${BLUE}4️⃣  추론 테스트:${NC}"
echo -e "   docker exec -it movie-rating-dev-container python src/main.py inference --data '[1,123,4508,7.5,1204.7]'"
echo -e ""

# 추가 도움말
echo -e "${YELLOW}추가 도움말:${NC}"
echo -e "   • README.md 파일에서 상세한 사용법 확인"
echo -e "   • .env 파일에서 TMDB_API_KEY 설정 필요"
echo -e "   • notebooks/ 폴더에서 Jupyter로 EDA 가능"
echo -e "   • 문제 발생시 GitHub Issues 활용"
echo -e ""

echo -e "${GREEN}Happy Coding! 영화 평점 예측 서비스를 만들어보세요!${NC}"