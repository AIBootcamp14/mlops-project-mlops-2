#!/bin/bash

# ==============================================
# Movie Rating MLOps - Environment Setup Script
# 영화 평점 예측 MLOps 환경 설정 스크립트
# ==============================================

set -e  # 에러 발생시 스크립트 종료

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}===============================================${NC}"
echo -e "${BLUE}  Movie Rating MLOps - Environment Setup${NC}"
echo -e "${BLUE}===============================================${NC}"

# 1. 환경변수 파일 설정
echo -e "\n${YELLOW}Step 1: 환경변수 파일 설정${NC}"

if [ -f ".env" ]; then
    echo -e "${YELLOW} .env 파일이 이미 존재합니다.${NC}"
    read -p "기존 .env 파일을 백업하고 새로 생성하시겠습니까? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        # 기존 파일 백업
        BACKUP_NAME=".env.backup.$(date +%Y%m%d_%H%M%S)"
        cp .env "$BACKUP_NAME"
        echo -e "${GREEN}기존 .env 파일을 ${BACKUP_NAME}으로 백업했습니다.${NC}"
        cp .env.template .env
    else
        echo -e "${BLUE}기존 .env 파일을 유지합니다.${NC}"
    fi
else
    echo -e "${GREEN}.env.template에서 .env 파일을 생성합니다.${NC}"
    cp .env.template .env
fi

# 2. 필수 디렉토리 생성 및 .gitkeep 파일 생성
echo -e "\n${YELLOW}Step 2: 프로젝트 디렉토리 구조 설정${NC}"

# 디렉토리 목록
directories=(
    "dataset/raw"
    "dataset/processed" 
    "dataset/external"
    "models"
    "notebooks"
    "config"
    "logs"
    "scripts"
)

echo -e "${BLUE}필요한 디렉토리들을 생성합니다...${NC}"

for dir in "${directories[@]}"; do
    if [ ! -d "$dir" ]; then
        mkdir -p "$dir"
        echo -e "${GREEN}생성: $dir/${NC}"
    else
        echo -e "${BLUE}존재: $dir/${NC}"
    fi
    
    # .gitkeep 파일 생성 (빈 파일)
    if [ ! -f "$dir/.gitkeep" ]; then
        touch "$dir/.gitkeep"
        echo -e "${GREEN}   └─ .gitkeep 파일 생성${NC}"
    fi
done

# 3. __init__.py 파일 생성
echo -e "\n${YELLOW}Step 3: Python 모듈 초기화 파일 생성${NC}"

# __init__.py가 필요한 디렉토리들
python_modules=(
    "src"
    "src/data"
    "src/model"
    "src/inference"
    "src/api"
    "src/utils"
)

echo -e "${BLUE}Python 모듈 초기화 파일들을 생성합니다...${NC}"

for module in "${python_modules[@]}"; do
    if [ ! -d "$module" ]; then
        mkdir -p "$module"
        echo -e "${GREEN}생성: $module/${NC}"
    fi
    
    if [ ! -f "$module/__init__.py" ]; then
        touch "$module/__init__.py"
        echo -e "${GREEN}   └─ __init__.py 파일 생성${NC}"
    else
        echo -e "${BLUE}   └─ __init__.py 파일 존재${NC}"
    fi
done

# 4. 환경변수 설정 안내
echo -e "\n${YELLOW}Step 4: 환경변수 설정 안내${NC}"
echo -e "${YELLOW}다음 환경변수들을 .env 파일에서 설정해주세요:${NC}"
echo -e ""
echo -e "${BLUE}필수 설정:${NC}"
echo -e "   TMDB_API_KEY=your_tmdb_api_key_here"
echo -e ""
echo -e "${BLUE}선택적 설정 (향후 사용):${NC}"
echo -e "   DB_USER=your_db_user"
echo -e "   DB_PASSWORD=your_db_password"
echo -e "   WANDB_API_KEY=your_wandb_api_key"
echo -e ""

# 5. 에디터로 .env 파일 열기 제안
echo -e "${YELLOW}지금 .env 파일을 편집하시겠습니까?${NC}"
read -p "   (v)im / (c)ode / (n)o: " -n 1 -r
echo
case $REPLY in
    v|V)
        if command -v vim &> /dev/null; then
            vim .env
        else
            echo -e "${RED}vim이 설치되어 있지 않습니다.${NC}"
        fi
        ;;
    c|C)
        if command -v code &> /dev/null; then
            code .env
        else
            echo -e "${RED}VS Code가 설치되어 있지 않습니다.${NC}"
        fi
        ;;
    *)
        echo -e "${BLUE}나중에 .env 파일을 직접 편집해주세요.${NC}"
        ;;
esac

# 6. 완료 메시지
echo -e "\n${BLUE}===============================================${NC}"
echo -e "${BLUE}  환경 설정 완료! 다음 단계를 진행하세요${NC}"
echo -e "${BLUE}===============================================${NC}"
echo -e "${GREEN}이미지 빌드: ./scripts/build_image.sh${NC}"
echo -e "${GREEN}컨테이너 실행: ./scripts/run_dev.sh${NC}"
echo -e "${GREEN}전체 가이드: ./scripts/quick_start.sh${NC}"