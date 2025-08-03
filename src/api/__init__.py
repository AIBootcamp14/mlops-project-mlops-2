
from fastapi import FastAPI
from contextlib import contextmanager

from src.api.middleware import register_middleware
from src.api.routers import train, predict
from src.ml.loader import load_mlflow_model
from src.utils.logger import get_logger

logger = get_logger(__name__)

mlflow_model = None

@contextmanager
def lifespan(app):
    global mlflow_model
    logger.info("서버 시작 Step")
    logger.info("[start] step1. load mlflow model")
    mlflow_model = load_mlflow_model(model_uri="models:/best_model/Production")
    logger.info("[end] step1. mlflow model loaded")

    yield

    logger.info("서버 종료")


app = FastAPI(lifespan=lifespan)

register_middleware(app)

app.include_router(train.router)
app.include_router(predict.router)


