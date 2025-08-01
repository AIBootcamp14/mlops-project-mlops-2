# 🎬 Movie Rating MLOps Project

> **영화 평점 예측 서비스** - TMDB API 기반 MLOps 파이프라인 구축 프로젝트

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/Docker-20.10+-blue.svg)](https://www.docker.com/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.0+-red.svg)](https://pytorch.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Latest-green.svg)](https://fastapi.tiangolo.com/)

## 📋 프로젝트 개요

**TMDB API**를 활용하여 영화 데이터를 수집하고, **PyTorch**로 평점 예측 모델을 개발하여 **FastAPI**로 서비스하는 **MLOps 파이프라인**을 구축합니다.

### 🎯 주요 목표
- **데이터 수집**: TMDB API를 통한 영화 정보 크롤링
- **모델 개발**: PyTorch 기반 영화 평점 예측 모델
- **서비스 배포**: FastAPI를 활용한 REST API 서비스  
- **MLOps 구현**: Docker 컨테이너 기반 개발/배포 환경

### 🛠️ 기술 스택
- **데이터**: TMDB API, pandas, numpy
- **모델**: PyTorch, scikit-learn
- **API**: FastAPI, uvicorn
- **인프라**: Docker, Airflow
- **협업**: Git, Jira

---

## 🚀 빠른 시작 (Quick Start)

### 0️⃣ 스크립트 실행 권한 설정 (Linux/macOS)

```bash
# 프로젝트 클론 후 처음 한 번만 실행
chmod +x scripts/*.sh

# 또는 권한 설정 스크립트 사용
bash scripts/setup_permissions.sh
```

### 1️⃣ 원클릭 설정 (추천)

```bash
# 프로젝트 클론
git clone <repository-url>
cd movie-rating-mlops

# 원클릭 환경 설정 및 실행
./scripts/quick_start.sh

# 또는 Makefile 사용 (더 간편)
make start
```

### 2️⃣ 단계별 설정

```bash
# 방법 1: 스크립트 사용
./scripts/setup_env.sh      # 환경 설정
./scripts/build_image.sh    # Docker 이미지 빌드  
./scripts/run_dev.sh        # 개발 컨테이너 실행

# 방법 2: Makefile 사용 (추천)
make setup                  # 환경 설정
make build                  # Docker 이미지 빌드
make run                    # 개발 컨테이너 실행
```

### 📋 Makefile 명령어 (편의 기능)

```bash
make help                   # 사용 가능한 명령어 보기
make start                  # 원클릭 전체 설정
make status                 # 프로젝트 상태 확인
make shell                  # 컨테이너 접속
make logs                   # 컨테이너 로그 확인
make clean                  # 환경 정리
```

---

## 📁 프로젝트 구조

```
movie-rating-mlops/
├── 🔧 scripts/                    # 실행 스크립트들
│   ├── quick_start.sh             # 원클릭 시작
│   ├── setup_env.sh              # 환경 설정
│   ├── build_image.sh            # 이미지 빌드
│   ├── run_dev.sh                # 컨테이너 실행
│   └── setup_permissions.sh      # 실행 권한 설정
│
├── 📦 src/                        # 소스 코드
│   ├── main.py                   # CLI 진입점 (Fire 기반)
│   ├── data/                     # 데이터 처리
│   │   ├── crawler.py           # TMDB API 크롤러
│   │   ├── preprocessor.py      # 데이터 전처리
│   │   └── feature_engineering.py
│   ├── model/                    # 모델 개발
│   │   ├── movie_predictor.py   # 평점 예측 모델
│   │   ├── trainer.py           # 모델 학습
│   │   └── evaluator.py         # 모델 평가
│   ├── api/                      # API 서버
│   │   ├── main.py              # FastAPI 서버
│   │   └── endpoints.py         # API 엔드포인트
│   └── utils/                    # 유틸리티
│
├── 📊 dataset/                    # 데이터셋
│   ├── raw/                      # 원본 데이터
│   ├── processed/                # 전처리된 데이터  
│   └── external/                 # 외부 데이터
│
├── 🤖 models/                     # 학습된 모델
├── 📓 notebooks/                  # Jupyter 노트북 (EDA)
├── ⚙️ config/                     # 설정 파일
├── 📝 logs/                       # 로그 파일
│
├── 🐳 Dockerfile                  # 컨테이너 환경
├── 📋 requirements.txt            # Python 의존성
├── 🔐 .env.template              # 환경변수 템플릿
├── 🛠️ Makefile                   # 자동화 명령어
└── 📖 README.md                   # 이 파일
```

---

## ⚙️ 환경 설정

### 🔑 필수 설정

#### 1. TMDB API 키 발급
1. [TMDB 개발자 사이트](https://developer.themoviedb.org/reference/intro/getting-started) 방문
2. 계정 생성 후 API 키 발급
3. `.env` 파일에 설정:

```bash
# .env 파일
TMDB_API_KEY=your_tmdb_api_key_here
TMDB_BASE_URL=https://api.themoviedb.org/3
TMDB_LANGUAGE=ko-KR
TMDB_REGION=KR
```

#### 2. 선택적 설정 (향후 사용)

```bash
# 데이터베이스 (향후 API 서버용)
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=3306

# 실험 추적 (향후 모델 개발용)
WANDB_API_KEY=your_wandb_api_key
```

### 🐳 Docker 환경

- **베이스 이미지**: `python:3.11-bookworm`
- **포트**: 8000 (메인), 8001 (백업)
- **볼륨 마운트**: 로컬 디렉토리 ↔ 컨테이너 `/workspace`

---

## 💻 사용법

### 🔗 컨테이너 접속

```bash
# 컨테이너 내부 접속
docker exec -it (컨테이너 이름) bash
```

### 📊 데이터 수집 및 전처리

```bash
# 데이터 수집 (TMDB API)
python src/main.py preprocessing --date 250101

# 실행 예시 (컨테이너 내부)
docker exec -it movie-rating-dev-container python src/main.py preprocessing --date 250101
```

### 🤖 모델 학습

```bash
# 모델 학습
python src/main.py train --model_name movie_predictor --num_epochs 50

# 실행 예시 (컨테이너 내부)  
docker exec -it movie-rating-dev-container python src/main.py train --model_name movie_predictor --num_epochs 50
```

### 🔮 모델 추론

```bash
# 단일 예측
python src/main.py inference --data "[1,123,4508,7.5,1204.7]" --batch_size 1

# 배치 예측
python src/main.py inference --batch_size 64
```

### 🌐 API 서버 실행 (향후)

```bash
# FastAPI 서버 실행
python src/api/main.py

# API 문서 확인
# http://localhost:8000/docs
```

---

## 👥 팀 협업

### 🔄 Git 워크플로우

```bash
# 1. 팀 저장소에서 포크
git clone -b dev https://github.com/AIBootcamp14/mlops-project-mlops-2.git

# 2. 개인 브랜치로 switch
git switch -c (개인 브랜치)

# 4. 작업 후 커밋
git add .
git commit -m "feat: 기능 설명"

# 5. 포크된 저장소에 푸시
git push origin feature/(개인 브랜치)

# 6. Pull Request 생성
```

### 📋 작업 관리 (Jira)

- **이슈 생성**: 각 기능별로 Jira 티켓 생성
- **브랜치 연동**: `feature/JIRA-123-description` 형식
- **진행 상황**: To Do → In Progress → Review → Done

### 🔍 코드 리뷰

- **모든 PR은 코드 리뷰 필수**
- **최소 1명 이상의 승인 필요**
- **CI/CD 파이프라인 통과 후 머지**

---

## 🛠️ 개발 가이드

### 📝 코딩 컨벤션

```python
# 모듈 import 순서
import os           # 표준 라이브러리
import sys

import requests     # 서드파티 라이브러리
import pandas as pd

from src.utils.config import Config  # 프로젝트 내부 모듈
```

### 🧪 테스트

```bash
# 단위 테스트 실행
python -m pytest tests/

# 특정 테스트 실행
python -m pytest tests/test_data_processing.py
```

### 📊 주피터 노트북 (EDA)

```bash
# 로컬에서 주피터 실행 (추천)
jupyter notebook notebooks/

# 또는 컨테이너에서 실행
docker exec -it movie-rating-dev-container jupyter notebook --ip=0.0.0.0 --port=8888 --no-browser --allow-root
```

---

## 🚨 트러블슈팅

### ❌ 자주 발생하는 문제들

#### 1. TMDB API 키 오류
```bash
ValueError: TMDB_API_KEY 환경변수가 설정되지 않았습니다.

해결: .env 파일에 TMDB_API_KEY=your_key_here 추가
```

#### 2. 포트 충돌
```bash
❌ 포트 8000이 이미 사용 중입니다.

해결: 스크립트가 자동으로 8001 포트로 전환하거나, 
     다른 서비스를 중지 후 재실행
```

#### 3. Docker 권한 오류
```bash
permission denied while trying to connect to the Docker daemon

해결: 
sudo usermod -a -G docker $USER
# 터미널 재시작 필요
```

#### 4. 컨테이너 빌드 실패
```bash
해결 순서:
1. Docker 데몬 실행 확인: docker ps
2. Dockerfile 경로 확인: 프로젝트 루트에서 실행
3. requirements.txt 확인: 파일 존재 및 문법 확인
```


## 📚 참고 자료

### 🔗 API 문서
- [TMDB API](https://developer.themoviedb.org/reference/intro/getting-started)
- [FastAPI 문서](https://fastapi.tiangolo.com/)

### 📖 기술 문서  
- [PyTorch 튜토리얼](https://pytorch.org/tutorials/)
- [Docker 가이드](https://docs.docker.com/)
- [MLOps 베스트 프랙티스](https://ml-ops.org/)

---

## 👨‍💻 기여자 (Contributors)

- **팀 리더**: 김 수환 (Suhwan KIM)
- **데이터 엔지니어**: 이 가은 (Kaeun LEE)
- **ML 엔지니어**: 김 병현 (Byeonghyeon KIM)
- **백엔드 개발자**: 이 윤서 (Yoonseo LEE)

---

**🚀 Happy Coding! 함께 멋진 영화 평점 예측 서비스를 만들어봅시다! 🎬**