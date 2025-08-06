from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
from contextlib import asynccontextmanager
import os
import sys

# 프로젝트 루트 경로 추가
sys.path.append(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)

from src.api.middleware import register_middleware
from src.api.routers import train, predict, reload, airflow
from src.ml.loader import get_model
from src.utils.logger import get_logger

logger = get_logger(__name__)

mlflow_model = None

@asynccontextmanager
async def lifespan(app):
    global mlflow_model
    logger.info("서버 시작 Step")
    logger.info("[START] loading mlflow model")

    # MLflow 모델 로딩 (에러 처리 추가)
    try:
        mlflow_model = get_model()
        logger.info(f"[END] mlflow model loaded successfully")
    except Exception as e:
        logger.warning(f"MLflow 모델 로딩 실패: {e}")
        logger.info("모델 없이 서버를 시작합니다.")
        mlflow_model = None

    yield

    logger.info("서버 종료")


# FastAPI 앱 생성
app = FastAPI(
    title="영화 평점 예측 서비스",
    description="MLOps 영화 평점 예측 API 및 웹 서비스",
    version="1.0.0",
    lifespan=lifespan
)

# 미들웨어 등록
register_middleware(app)

# API 라우터 등록
app.include_router(train.router)
app.include_router(predict.router)
app.include_router(reload.router)
app.include_router(airflow.router)

# 프로젝트 루트 경로 계산
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
frontend_path = os.path.join(project_root, "frontend")

logger.info(f"프로젝트 루트: {project_root}")
logger.info(f"프론트엔드 경로: {frontend_path}")
logger.info(f"프론트엔드 경로 존재 여부: {os.path.exists(frontend_path)}")

# 정적 파일 서빙 (에러 처리 추가)
if os.path.exists(os.path.join(frontend_path, "assets")):
    app.mount("/static", StaticFiles(directory=os.path.join(frontend_path, "assets")), name="static")
    logger.info("✅ 정적 파일 경로 마운트 완료")
else:
    logger.warning("⚠️ frontend/assets 디렉토리가 존재하지 않습니다.")

# 간단한 HTML 응답 함수들
def get_simple_html(title, message):
    return f"""
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="UTF-8">
        <title>{title}</title>
        <style>
            body {{ font-family: 'Malgun Gothic', sans-serif; 
                   background: #f5f6fa; 
                   display: flex; 
                   justify-content: center; 
                   align-items: center; 
                   height: 100vh; 
                   margin: 0; }}
            .container {{ background: #fff; 
                         border-radius: 12px; 
                         padding: 40px 30px; 
                         box-shadow: 0 2px 12px rgba(0,0,0,0.07); 
                         text-align: center; }}
            h1 {{ color: #27408b; margin-bottom: 24px; }}
            p {{ color: #666; line-height: 1.6; }}
            .btn {{ display: inline-block; 
                   background: #27408b; 
                   color: #fff; 
                   padding: 12px 24px; 
                   border: none; 
                   border-radius: 6px; 
                   text-decoration: none; 
                   margin: 10px; }}
            .btn:hover {{ background: #4169e1; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>{title}</h1>
            <p>{message}</p>
            <a href="/docs" class="btn">API 문서 보기</a>
            <a href="/predict/sample" class="btn">샘플 예측 테스트</a>
            <a href="/survey" class="btn">영화 평점 예측하기</a>
        </div>
    </body>
    </html>
    """

# 웹페이지 라우트 추가
@app.get("/")
async def root():
    """메인 페이지"""
    login_html_path = os.path.join(frontend_path, "login.html")
    
    if os.path.exists(login_html_path):
        return FileResponse(login_html_path)
    else:
        html_content = get_simple_html(
            "영화 평점 예측 서비스",
            "MLOps 프로젝트의 영화 평점 예측 서비스입니다."
        )
        return HTMLResponse(content=html_content)

@app.get("/login")
@app.get("/login.html")
async def login_page():
    """로그인 페이지"""
    login_html_path = os.path.join(frontend_path, "login.html")
    
    if os.path.exists(login_html_path):
        return FileResponse(login_html_path)
    else:
        html_content = """
        <!DOCTYPE html>
        <html lang="ko">
        <head>
            <meta charset="UTF-8">
            <title>로그인 - 영화 평점 예측</title>
            <style>
                body { font-family: 'Malgun Gothic', sans-serif; background: #f5f6fa; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0;}
                .login-container { background: #fff; border-radius: 12px; padding: 40px 30px; box-shadow: 0 2px 12px rgba(0,0,0,0.07); min-width: 300px;}
                h2 { margin-bottom: 24px; color: #27408b; text-align: center;}
                label { display: block; margin-bottom: 8px; }
                input[type="text"], input[type="password"] { width: 100%; padding: 10px; margin-bottom: 20px; border-radius: 6px; border: 1px solid #ccc; box-sizing: border-box;}
                button { width: 100%; background: #27408b; color: #fff; padding: 12px; border: none; border-radius: 6px; font-size: 16px; cursor: pointer; }
                button:hover { background: #4169e1;}
            </style>
        </head>
        <body>
            <div class="login-container">
                <h2>로그인</h2>
                <form id="login-form">
                    <label for="userid">아이디</label>
                    <input type="text" id="userid" required>
                    <label for="userpw">비밀번호</label>
                    <input type="password" id="userpw" required>
                    <button type="submit">로그인</button>
                </form>
            </div>
            <script>
                document.getElementById('login-form').addEventListener('submit', function(e){
                    e.preventDefault();
                    window.location.href = '/survey';
                });
            </script>
        </body>
        </html>
        """
        return HTMLResponse(content=html_content)

@app.get("/survey")
@app.get("/survey.html")
async def survey_page():
    """개선된 영화 정보 입력 설문 페이지 - 19개 장르 + 인라인 결과"""
    # frontend 디렉토리에 survey.html이 있으면 그것을 사용하지 않고 무조건 새 버전 사용
    html_content = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>영화 정보 입력 - 평점 예측</title>
    <style>
        body { 
            font-family: 'Malgun Gothic', sans-serif; 
            background: #f5f6fa; 
            display: flex; 
            justify-content: center; 
            align-items: center; 
            min-height: 100vh; 
            margin: 0; 
            padding: 20px; 
            box-sizing: border-box;
        }
        .survey-container { 
            background: #fff; 
            border-radius: 12px; 
            padding: 40px 30px; 
            box-shadow: 0 2px 12px rgba(0,0,0,0.07); 
            max-width: 600px; 
            width: 100%;
        }
        h2 { 
            margin-bottom: 24px; 
            color: #27408b; 
            text-align: center;
        }
        label { 
            display: block; 
            margin-bottom: 8px; 
            margin-top: 16px; 
            font-weight: bold;
        }
        input, select, textarea { 
            width: 100%; 
            padding: 10px; 
            border-radius: 6px; 
            border: 1px solid #ccc; 
            margin-bottom: 10px; 
            box-sizing: border-box;
            font-size: 14px;
        }
        .checkbox-group { 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); 
            gap: 10px; 
            margin-bottom: 15px;
            max-height: 200px;
            overflow-y: auto;
            border: 1px solid #eee;
            padding: 15px;
            border-radius: 6px;
            background: #f9f9f9;
        }
        .checkbox-group label { 
            margin: 0; 
            font-weight: normal; 
            display: flex; 
            align-items: center;
            font-size: 13px;
            cursor: pointer;
        }
        .checkbox-group input { 
            width: auto; 
            margin-right: 8px;
            margin-bottom: 0;
        }
        .checkbox-group label:hover {
            background: #e3f2fd;
            border-radius: 4px;
            padding: 2px;
        }
        button { 
            width: 100%; 
            background: #27408b; 
            color: #fff; 
            padding: 15px; 
            border: none; 
            border-radius: 6px; 
            font-size: 16px; 
            cursor: pointer; 
            margin-top: 10px;
            transition: background 0.3s;
        }
        button:hover { 
            background: #4169e1;
        }
        button:disabled {
            background: #ccc;
            cursor: not-allowed;
        }
        .result { 
            margin-top: 20px; 
            padding: 20px; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 10px; 
            text-align: center;
            color: white;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
            display: none;
            animation: slideIn 0.5s ease-out;
        }
        @keyframes slideIn {
            from {
                opacity: 0;
                transform: translateY(-20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        .result h3 {
            margin: 0 0 10px 0;
            font-size: 18px;
        }
        .result .score {
            font-size: 32px;
            font-weight: bold;
            margin: 10px 0;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        .result .method {
            font-size: 12px;
            opacity: 0.8;
            margin-top: 10px;
        }
        .status { 
            padding: 12px; 
            margin-bottom: 20px; 
            border-radius: 6px; 
            text-align: center; 
            font-size: 14px;
        }
        .status.warning { 
            background: #fff3cd; 
            color: #856404; 
            border: 1px solid #ffeaa7;
        }
        .status.ok {
            background: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }
        .loading {
            display: none;
            text-align: center;
            margin-top: 10px;
        }
        .loading::after {
            content: "";
            display: inline-block;
            width: 20px;
            height: 20px;
            border: 3px solid #f3f3f3;
            border-top: 3px solid #27408b;
            border-radius: 50%;
            animation: spin 1s linear infinite;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        .genre-count {
            font-size: 12px;
            color: #666;
            margin-top: 5px;
        }
    </style>
</head>
<body>
    <div class="survey-container">
        <h2>🎬 영화 평점 예측</h2>
        
        <div class="status warning" id="model-status">
            ⚠️ 상태 확인 중...
        </div>
        
        <form id="survey-form">
            <label>성인영화 여부</label>
            <select name="adult">
                <option value="">선택안함</option>
                <option value="0">아니오</option>
                <option value="1">예</option>
            </select>
            
            <label>장르 (복수 선택 가능)</label>
            <div class="checkbox-group">
                <label><input type="checkbox" name="genre_ids" value="28"> 액션</label>
                <label><input type="checkbox" name="genre_ids" value="12"> 모험</label>
                <label><input type="checkbox" name="genre_ids" value="16"> 애니메이션</label>
                <label><input type="checkbox" name="genre_ids" value="35"> 코미디</label>
                <label><input type="checkbox" name="genre_ids" value="80"> 범죄</label>
                <label><input type="checkbox" name="genre_ids" value="99"> 다큐멘터리</label>
                <label><input type="checkbox" name="genre_ids" value="18"> 드라마</label>
                <label><input type="checkbox" name="genre_ids" value="10751"> 가족</label>
                <label><input type="checkbox" name="genre_ids" value="14"> 판타지</label>
                <label><input type="checkbox" name="genre_ids" value="36"> 역사</label>
                <label><input type="checkbox" name="genre_ids" value="27"> 공포</label>
                <label><input type="checkbox" name="genre_ids" value="10402"> 음악</label>
                <label><input type="checkbox" name="genre_ids" value="9648"> 미스터리</label>
                <label><input type="checkbox" name="genre_ids" value="10749"> 로맨스</label>
                <label><input type="checkbox" name="genre_ids" value="878"> SF</label>
                <label><input type="checkbox" name="genre_ids" value="10770"> TV 영화</label>
                <label><input type="checkbox" name="genre_ids" value="53"> 스릴러</label>
                <label><input type="checkbox" name="genre_ids" value="10752"> 전쟁</label>
                <label><input type="checkbox" name="genre_ids" value="37"> 서부</label>
            </div>
            <div class="genre-count" id="genre-count">선택된 장르: 0개</div>
            
            <label>원어(언어)</label>
            <select name="original_language">
                <option value="">선택안함</option>
                <option value="ko">한국어</option>
                <option value="en">영어</option>
                <option value="ja">일본어</option>
                <option value="zh">중국어</option>
                <option value="fr">프랑스어</option>
                <option value="de">독일어</option>
                <option value="es">스페인어</option>
            </select>
            
            <label>줄거리</label>
            <textarea name="overview" rows="4" placeholder="영화 줄거리를 자세히 입력해주세요. 더 자세할수록 예측 정확도가 높아집니다!"></textarea>
            
            <label>비디오 여부</label>
            <select name="video">
                <option value="">선택안함</option>
                <option value="0">극장 개봉</option>
                <option value="1">직접 배급 (넷플릭스, OTT 등)</option>
            </select>
            
            <button type="submit" id="predict-btn">🎯 평점 예측하기</button>
            <div class="loading" id="loading">예측 중...</div>
        </form>
        
        <div id="result" class="result">
            <h3>🎬 예측 결과</h3>
            <div class="score" id="pred-score"></div>
            <div id="pred-message"></div>
            <div class="method" id="pred-method"></div>
        </div>
    </div>
    
    <script>
        // 서버 상태 확인
        fetch('/predict/health')
            .then(r => r.json())
            .then(data => {
                const statusEl = document.getElementById('model-status');
                if (data.model_loaded) {
                    statusEl.className = 'status ok';
                    statusEl.innerHTML = '🤖 <strong>ML 모델 활성</strong> - 실제 머신러닝 예측';
                } else {
                    statusEl.className = 'status warning';
                    statusEl.innerHTML = '⚠️ <strong>폴백 모드</strong> - 규칙 기반 예측 (정확도 약 70-80%)';
                }
            })
            .catch(e => {
                document.getElementById('model-status').innerHTML = '❌ 서버 상태 확인 실패';
            });

        // 장르 선택 카운터
        document.addEventListener('change', function(e) {
            if (e.target.name === 'genre_ids') {
                const checkedGenres = document.querySelectorAll('input[name="genre_ids"]:checked');
                document.getElementById('genre-count').textContent = `선택된 장르: ${checkedGenres.length}개`;
            }
        });

        // 폼 제출 처리
        document.getElementById('survey-form').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const form = e.target;
            const predictBtn = document.getElementById('predict-btn');
            const loading = document.getElementById('loading');
            const resultDiv = document.getElementById('result');
            
            // UI 상태 변경
            predictBtn.disabled = true;
            predictBtn.textContent = '예측 중...';
            loading.style.display = 'block';
            resultDiv.style.display = 'none';
            
            // 폼 데이터 수집
            const adult = form.adult.value === "" ? null : Number(form.adult.value);
            const original_language = form.original_language.value === "" ? null : form.original_language.value;
            const overview = form.overview.value.trim() === "" ? null : form.overview.value.trim();
            const video = form.video.value === "" ? null : Number(form.video.value);
            
            const genreNodes = form.querySelectorAll('input[name="genre_ids"]:checked');
            const genre_ids = Array.from(genreNodes).map(x => Number(x.value));

            const payload = {
                adult, 
                genre_ids: genre_ids.length ? genre_ids : null, 
                original_language, 
                overview, 
                video
            };

            try {
                const res = await fetch('/predict/json', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(payload)
                });
                
                if (!res.ok) {
                    throw new Error(`서버 오류: ${res.status}`);
                }
                
                const data = await res.json();
                
                // 결과 표시
                document.getElementById('pred-score').textContent = `${data.pred}점`;
                
                // 점수에 따른 메시지
                let message = '';
                if (data.pred >= 8.5) {
                    message = '🏆 최고 수작! 꼭 봐야 할 영화';
                } else if (data.pred >= 7.5) {
                    message = '⭐ 훌륭한 작품! 추천합니다';
                } else if (data.pred >= 6.5) {
                    message = '👍 괜찮은 영화입니다';
                } else if (data.pred >= 5.5) {
                    message = '😐 평범한 수준입니다';
                } else {
                    message = '😞 아쉬운 작품일 수 있어요';
                }
                
                document.getElementById('pred-message').textContent = message;
                document.getElementById('pred-method').textContent = data.message || '';
                
                // 결과 표시
                resultDiv.style.display = 'block';
                
                // 결과로 스크롤
                resultDiv.scrollIntoView({ behavior: 'smooth' });
                
            } catch (err) {
                alert(`예측 실패: ${err.message}\\n\\n서버 상태를 확인해주세요.`);
            } finally {
                // UI 상태 복원
                predictBtn.disabled = false;
                predictBtn.textContent = '🎯 평점 예측하기';
                loading.style.display = 'none';
            }
        });

        // 엔터키로 폼 제출 방지 (textarea 제외)
        document.addEventListener('keypress', function(e) {
            if (e.key === 'Enter' && e.target.tagName !== 'TEXTAREA') {
                e.preventDefault();
            }
        });
    </script>
</body>
</html>"""
    
    return HTMLResponse(content=html_content)

# 헬스체크 엔드포인트
@app.get("/health")
async def health_check():
    """서버 상태 확인"""
    try:
        model = get_model()
        model_loaded = model is not None
    except:
        model_loaded = False
        
    return {
        "status": "healthy",
        "model_loaded": model_loaded,
        "service": "영화 평점 예측 서비스",
        "frontend_available": os.path.exists(frontend_path)
    }

# 전역 변수로 mlflow_model을 앱에서 접근 가능하게 만들기
def get_mlflow_model():
    """MLflow 모델 인스턴스 반환"""
    return mlflow_model