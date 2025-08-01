# ==============================================
# Movie Rating MLOps Project - Makefile
# 영화 평점 예측 MLOps 프로젝트 자동화
# ==============================================

.PHONY: help setup permissions build run start clean test

# 기본 타겟 (help 표시)
help:
	@echo "🎬 Movie Rating MLOps - Available Commands"
	@echo "=============================================="
	@echo "make setup        - 환경 설정 (환경변수, 디렉토리)"
	@echo "make permissions  - 스크립트 실행 권한 설정"
	@echo "make build        - Docker 이미지 빌드"
	@echo "make run          - 개발 컨테이너 실행"
	@echo "make start        - 전체 설정 및 실행 (원클릭)"
	@echo "make clean        - 컨테이너 및 이미지 정리"
	@echo "make test         - 테스트 실행"
	@echo ""
	@echo "🚀 빠른 시작: make start"

# 실행 권한 설정
permissions:
	@echo "🔧 스크립트 실행 권한 설정 중..."
	@chmod +x scripts/*.sh
	@echo "✅ 실행 권한 설정 완료!"

# 환경 설정
setup: permissions
	@echo "⚙️ 환경 설정 시작..."
	@./scripts/setup_env.sh

# Docker 이미지 빌드
build: permissions
	@echo "🐳 Docker 이미지 빌드 시작..."
	@./scripts/build_image.sh

# 개발 컨테이너 실행
run: permissions
	@echo "🚀 개발 컨테이너 실행 시작..."
	@./scripts/run_dev.sh

# 원클릭 시작 (전체 프로세스)
start: permissions
	@echo "🎬 Movie Rating MLOps 원클릭 시작!"
	@./scripts/quick_start.sh

# 정리 (컨테이너 및 이미지 삭제)
clean:
	@echo "🧹 환경 정리 중..."
	@-docker stop movie-rating-dev-container 2>/dev/null || true
	@-docker rm movie-rating-dev-container 2>/dev/null || true
	@-docker rmi movie-rating-dev:latest 2>/dev/null || true
	@echo "✅ 정리 완료!"

# 테스트 실행 (향후 구현)
test:
	@echo "🧪 테스트 실행..."
	@echo "⚠️  TODO: 테스트 코드 구현 필요"

# 컨테이너 내부 접속
shell:
	@echo "🔗 컨테이너에 접속합니다..."
	@docker exec -it movie-rating-dev-container bash

# 컨테이너 로그 확인
logs:
	@echo "📝 컨테이너 로그를 확인합니다..."
	@docker logs movie-rating-dev-container

# 상태 확인
status:
	@echo "📊 프로젝트 상태 확인..."
	@echo ""
	@echo "🐳 Docker 이미지:"
	@docker images | grep movie-rating || echo "   이미지 없음"
	@echo ""
	@echo "📦 실행 중인 컨테이너:"
	@docker ps | grep movie-rating || echo "   실행 중인 컨테이너 없음"
	@echo ""
	@echo "📁 프로젝트 파일:"
	@ls -la .env 2>/dev/null && echo "   ✅ .env 파일 존재" || echo "   ❌ .env 파일 없음"
	@ls -la Dockerfile 2>/dev/null && echo "   ✅ Dockerfile 존재" || echo "   ❌ Dockerfile 없음"