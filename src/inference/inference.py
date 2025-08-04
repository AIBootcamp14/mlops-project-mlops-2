import os
import sys
import joblib

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.dirname(
                os.path.abspath(__file__)
            )
        )
    )
)

from src.utils.utils import model_dir
from src.dataset.movie_rating import MovieRatingDataset, GenreEmbeddingModule


def load_checkpoint():
    target_dir = model_dir('checkpoint.pkl')
    checkpoint = joblib.load(target_dir)
    return checkpoint

def init_model(checkpoint):
    model = checkpoint.get('model', None)
    tf_idf = checkpoint.get("tf_idf", None)
    embedding_module = checkpoint.get("embedding_module", None)
    genre2idx = checkpoint.get("genre2idx", None)
    return model, tf_idf, embedding_module, genre2idx