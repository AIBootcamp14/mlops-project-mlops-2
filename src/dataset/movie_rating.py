import os
import sys
import re
from collections import defaultdict
import json

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))))
)

import pandas as pd
import numpy as np
from konlpy.tag import Okt
import torch
import torch.nn as nn
import torch.nn.utils.rnn as rnn_utils
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split



from src.utils.utils import project_path


class GenreEmbeddingModule(nn.Module):
    def __init__(self, genre_id_set, emb_dim=32):
        super().__init__()

        # 장르 인덱싱 + UNK
        genre2idx = {g: idx + 1 for idx, g in enumerate(sorted(genre_id_set))}  # 1부터 시작
        genre2idx['UNK'] = 0  # 0번은 패딩/UNK 용
        self.genre2idx = defaultdict(lambda: 0, genre2idx)  # default to UNK

        self.embedding = nn.Embedding(num_embeddings=len(genre2idx), embedding_dim=emb_dim, padding_idx=0)

    def get_genre2idx(self):
        return dict(self.genre2idx)

    def forward(self, genre_ids_batch):
        """
        genre_ids_batch: List[List[int]]
        Returns: Tensor [batch_size, emb_dim]
        """
        # 인덱스 매핑
        mapped_ids = [[self.genre2idx[g] for g in row] for row in genre_ids_batch]
        mapped_tensors = [torch.tensor(row, dtype=torch.long) for row in mapped_ids]

        # 패딩 적용
        padded = rnn_utils.pad_sequence(mapped_tensors, batch_first=True)  # [batch, max_len]
        device = self.embedding.weight.device
        padded = padded.to(device)

        # 임베딩
        emb = self.embedding(padded)  # [batch, max_len, emb_dim]

        # 마스크를 이용한 평균
        mask = (padded != 0).unsqueeze(-1)        # [batch, max_len, 1]
        masked = emb * mask                       # [batch, max_len, emb_dim]
        summed = masked.sum(dim=1)                # [batch, emb_dim]
        count = mask.sum(dim=1).clamp(min=1)      # [batch, 1]
        mean_emb = summed / count                 # [batch, emb_dim]

        return mean_emb


class MovieRatingDataset:
    def __init__(self, df, tf_idf = None, embedding_module = None):
        self.df = df
        self.features = None
        self.target = None
        self.tf_idf = tf_idf
        self.embedding_module = embedding_module
        self.okt = Okt()
        self._preprocessing()

    def genre_embedding(self, emb_dim:int = 32):
        genre_set = set(g for row in self.df['genre_ids'] for g in row)

    # ✅ 모델 정의 및 GPU로 이동
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        embedding_module = GenreEmbeddingModule(genre_set, emb_dim=emb_dim).to(device)

        return embedding_module

    def tensor_to_df(self, tensor_or_array, prefix, index):
        if isinstance(tensor_or_array, torch.Tensor):
            data = tensor_or_array.cpu().detach().numpy()
        else:
            data = tensor_or_array
        return pd.DataFrame(data, columns=[f"{prefix}_{i}" for i in range(data.shape[1])], index=index)


    # tfidf_df
    def clean_korean_text(self, text):
        text = re.sub(r'[^가-힣\s]', '', str(text))
        return text.strip()
    

    def okt_tokenizer(self, text):
        return self.okt.nouns(text)


    def overview_tf_idf(self, max_features:int = 300):
        vectorizer = TfidfVectorizer(tokenizer=self.okt_tokenizer, max_features=max_features)
        vectorizer.fit(self.df['overview_clean'])
        return vectorizer


    def _preprocessing(self):
        self.df['overview_clean'] = self.df['overview'].fillna("").apply(self.clean_korean_text)

        # genre embedding
        if self.embedding_module:
            genre_vecs = self.embedding_module(self.df['genre_ids'].tolist())
            genre_emb_df = self.tensor_to_df(genre_vecs, "emb", self.df.index)
        else:
            self.embedding_module = self.genre_embedding()
            genre_vecs = self.embedding_module(self.df['genre_ids'].tolist())
            genre_emb_df = self.tensor_to_df(genre_vecs, "emb", self.df.index)
            
        # overview tf-idf
        if self.tf_idf:
            X_tfidf = self.tf_idf.transform(self.df['overview_clean'])
            tfidf_df = self.tensor_to_df(X_tfidf.toarray(), "tfidf", self.df.index)
        else:
            self.tf_idf = self.overview_tf_idf()
            X_tfidf = self.tf_idf.transform(self.df['overview_clean'])
            tfidf_df = self.tensor_to_df(X_tfidf.toarray(), "tfidf", self.df.index)
            
        self.df['adult'] = self.df['adult'].astype('int')
        self.df['video'] = self.df['video'].astype("int")

        drop_features = ["backdrop_path", "id", "genre_ids", "original_title",
                          "title", "vote_count", "poster_path", "release_date",
                          "overview", "popularity",'overview_clean', 'original_language', 'vote_average']
        self.df['is_english'] = (self.df["original_language"] == 'en').astype(int)

        self.target = self.df['vote_average']
        self.features = pd.concat([self.df, tfidf_df, genre_emb_df], axis = 1).drop(columns = drop_features, axis = 1)
        

    @property
    def genre2idx(self):
        if self.embedding_module:
            return self.embedding_module.get_genre2idx()
        return {}
        
    @property
    def features_dim(self):
        return self.features.shape[1]


    def __len__(self):
        return len(self.target)

    def __getitem__(self, idx):
        return self.features.iloc[idx].values, self.target.iloc[idx]

def read_dataset():
    movie_rating_path = os.path.join(project_path(),"data-prepare","result")
    with open(movie_rating_path +"/popular.json","r", encoding= 'utf-8')as f:
        data = json.load(f)
    df = pd.DataFrame(data['movies'])
    return df

def split_dataset(df):
    train_df, val_df = train_test_split(df, test_size=0.2, random_state=42)
    train_df, test_df = train_test_split(train_df, test_size=0.2, random_state=42)
    return train_df, val_df, test_df


def get_datasets(tf_idf = None, embedding_module = None):
    df = read_dataset()
    train_df, val_df, test_df = split_dataset(df)
    train_dataset = MovieRatingDataset(train_df, tf_idf = tf_idf, embedding_module = embedding_module)
    val_dataset = MovieRatingDataset(val_df, tf_idf = train_dataset.tf_idf, embedding_module = train_dataset.embedding_module)
    test_dataset = MovieRatingDataset(test_df, tf_idf = train_dataset.tf_idf, embedding_module = train_dataset.embedding_module)
    return train_dataset, val_dataset, test_dataset


if __name__ == "__main__":
    print('test 중 입니다.')
    train, valid, test = get_datasets()
    print("train set 첫번째 행 : ", train[0])
    print("valid set 첫번째 행 : ", valid[0])
    print("test set 첫번째 행 : ", test[0])