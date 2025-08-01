#!/bin/bash

# ==============================================
# Movie Rating MLOps - Script Permissions Setup
# 영화 평점 예측 MLOps 스크립트 실행 권한 설정
# ==============================================

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}===============================================${NC}"
echo -e "${BLUE}  Movie Rating MLOps - Script Permissions${NC}"
echo -e "${BLUE}===============================================${NC}"

# 스크립트 파일 목록
scripts=(
    "scripts/setup_env.sh"
    "scripts/build_image.sh"
    "scripts/run_dev.sh"
    "scripts/quick_start.sh"
    "scripts/setup_permissions.sh"
)

echo -e "\n${YELLOW}📍 스크립트 실행 권한을 설정합니다...${NC}"

# 각 스크립트에 실행 권한 부여
for script in "${scripts[@]}"; do
    if [ -f "$script" ]; then
        chmod +x "$script"
        echo -e "${GREEN}✅ $script${NC}"
    else
        echo -e "${RED}❌ $script (파일을 찾을 수 없습니다)${NC}"
    fi
done

# 권한 확인
echo -e "\n${YELLOW}📍 설정된 권한 확인:${NC}"
for script in "${scripts[@]}"; do
    if [ -f "$script" ]; then
        permissions=$(ls -la "$script" | awk '{print $1}')
        echo -e "${BLUE}$script: $permissions${NC}"
    fi
done

echo -e "\n${GREEN}✅ 스크립트 실행 권한 설정 완료!${NC}"
echo -e "${YELLOW}💡 이제 다음과 같이 실행할 수 있습니다:${NC}"
echo -e "   ./scripts/quick_start.sh"
echo -e "   ./scripts/setup_env.sh"
echo -e "   ./scripts/build_image.sh"
echo -e "   ./scripts/run_dev.sh"