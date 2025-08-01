#!/usr/bin/env python3
"""
Movie Rating MLOps Project - Main Entry Point
영화 평점 예측 MLOps 프로젝트 메인 진입점

실습에서 사용한 Fire 기반 CLI 인터페이스
사용법:
    python src/main.py preprocessing --date 250101
    python src/main.py train --model_name movie_predictor --num_epochs 50
    python src/main.py inference --data "[1,123,4508,7.5,1204.7]" --batch_size 1
"""