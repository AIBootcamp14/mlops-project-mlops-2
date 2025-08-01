# 🎬 Movie Rating MLOps - Development Guide

> **영화 평점 예측 MLOps 프로젝트** - 개발 브랜치 (dev)

## 🚀 빠른 시작

### 1️⃣ 프로젝트 클론 및 개인 브랜치 생성

```bash
# dev 브랜치 클론
git clone -b dev https://github.com/AIBootcamp14/mlops-project-mlops-2.git
cd mlops-project-mlops-2

# 개인 브랜치 생성 및 전환
git switch -c <개인브랜치명>
# 예시: git switch -c feature/Byeonghyeon
```

### 2️⃣ 개발 환경 구성

```bash
# 원클릭 환경 설정
make start

# 또는 단계별 설정
make setup      # 환경 설정
make build      # Docker 이미지 빌드  
make run        # 컨테이너 실행
```

### 3️⃣ 개발 진행

```bash
# 컨테이너 접속하여 개발
make shell

# 또는 직접 명령 실행
docker exec -it movie-rating-dev-container python src/main.py preprocessing --date 250101
```

## 📋 Git 협업 워크플로우

### 🔄 일반적인 개발 사이클

```bash
# 1. 작업 전 최신 dev 반영
git checkout dev
git pull origin dev
git checkout <개인브랜치명>
git merge dev

# 2. 개발 진행 후 커밋
git add .
git commit -m "feat: 영화 크롤러 구현"

# 3. 개인 브랜치에 푸시
git push origin <개인브랜치명>

# 4. GitHub에서 PR 생성
# dev ← <개인브랜치명> 으로 Pull Request
```

### 📁 서버에서 작업하는 경우

**서버 VS Code에서 clone 했다면:**
- clone한 디렉토리 = 개인 작업공간
- Docker 구성, Python 실행 등 **자유롭게 사용**
- **commit한 것만 push**되므로 commit/push만 신중하게

### 🔀 브랜치 전략

```
main (배포)
  ↑
 dev (개발 통합)
  ↑
feature/개인브랜치들 (개별 개발)
```

## 💡 개발 팁

### 🎯 커밋 메시지 컨벤션
```bash
feat: 새로운 기능 추가
fix: 버그 수정  
docs: 문서 수정
style: 코드 포맷팅
refactor: 코드 리팩토링
test: 테스트 추가/수정
```

### 📂 파일별 작업 분담 예시
```bash
# 데이터 담당자
git add src/data/
git commit -m "feat: TMDB API 크롤러 구현"

# 모델 담당자  
git add src/model/
git commit -m "feat: PyTorch 평점 예측 모델 구현"

# API 담당자
git add src/api/
git commit -m "feat: FastAPI 엔드포인트 구현"
```

## 🚨 주의사항

### ❌ Git에 올리면 안 되는 것들
- `.env` 파일 (API 키 포함)
- `models/*.pkl` 파일 (용량 큰 모델)
- `dataset/raw/` 데이터 (원본 데이터)
- `__pycache__/` 폴더

### ✅ 반드시 올려야 하는 것들
- 소스 코드 (`src/`)
- 설정 파일 (`.env.template`, `Dockerfile`)
- 문서 (`README.md`, 주석)
- 테스트 코드 (`tests/`)

## 🔧 자주 사용하는 명령어

```bash
# 프로젝트 상태 확인
make status

# 컨테이너 접속
make shell

# 컨테이너 로그 확인  
make logs

# 환경 정리
make clean

# Git 상태 확인
git status
git branch -a
```


**🎬 함께 멋진 영화 평점 예측 서비스를 만들어봅시다!**