# ==============================================
# Movie Rating MLOps Project - Dockerfile
# 영화 평점 예측 MLOps 프로젝트 컨테이너 환경
# ==============================================

# Python 3.11 bookworm 기반 이미지 사용
FROM python:3.11-bookworm

# Python 의존성 설치 (실습 방식)
COPY requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt

# 프로젝트 구조 복사 (배포시 사용)
COPY dataset /opt/dataset
COPY src /opt/src
COPY config /opt/config
COPY scripts /opt/scripts

# 실행 스크립트 복사 (향후 API 서버용)
# COPY start_api_server.sh /opt

# 작업 디렉토리 설정
WORKDIR /opt

# 포트 설정 (향후 API 서버용)
EXPOSE 8000
EXPOSE 8001

# 주석: .env 파일은 보안상 이미지에 포함하지 않음
# 컨테이너 실행시 볼륨 마운트나 환경변수로 전달
# docker run -e TMDB_API_KEY=<key> -e DB_USER=<user> ...