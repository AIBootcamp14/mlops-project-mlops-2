import csv
import ast
import pandas as pd


class MoviePreprocessor:
    def __init__(self, filepath, max_error_ratio=0.01):
        self.filepath = filepath
        self.max_error_ratio = max_error_ratio
        self.df = None
        self.error_rows = []

    def load_csv(self):
        rows = []
        error_rows = []

        with open(self.filepath, "r", encoding="utf-8-sig") as f:
            reader = csv.reader(f, quotechar='"')
            header = next(reader)
            for i, row in enumerate(reader, start=2):
                try:
                    if len(row) != len(header):
                        raise ValueError("Column count mismatch")
                    rows.append(row)
                except Exception as e:
                    error_rows.append((i, str(e), row))

        total = len(rows) + len(error_rows)
        error_ratio = len(error_rows) / total
        if error_ratio > self.max_error_ratio:
            raise ValueError(f"❌ Too many malformed rows: {len(error_rows)} / {total} ({error_ratio:.2%})")

        self.df = pd.DataFrame(rows, columns=header)
        self.error_rows = error_rows
        return self.df

    def save_error_log(self, path="error_rows_log.csv"):
        pd.DataFrame(self.error_rows, columns=["line", "error", "row"]).to_csv(path, index=False)

    def drop_unused_columns(self):
        cols_to_drop = ['id', 'original_title', 'overview', 'genre_ids', 'popularity', 'vote_count']
        self.df.drop(columns=cols_to_drop, inplace=True, errors='ignore')
        return self

    def create_release_month(self):
        self.df["release_date"] = pd.to_datetime(self.df['release_date'], errors='coerce')
        self.df['release_month'] = self.df["release_date"].dt.month
        return self

    def create_monthly_avg_score(self):
        try:
            self.df['vote_average'] = self.df['vote_average'].astype(float)
        except:
            pass
        month_avg = self.df.groupby('release_month')['vote_average'].mean()
        self.df['month_avg_score'] = self.df['release_month'].map(month_avg)
        return self

    def create_genre_avg_score(self):
        self.df["genres"] = self.df["genres"].apply(ast.literal_eval)
        genre_scores = (
            self.df.explode("genres")
                .groupby("genres")["vote_average"]
                .mean()
                .to_dict()
        )
        self.df["genre_avg_score"] = self.df["genres"].apply(
            lambda genre_list: sum([genre_scores.get(g, 0) for g in genre_list]) / len(genre_list)
            if genre_list else 0
        )
        return self

    def create_director_avg_score(self):
        self.df["directors"] = self.df["directors"].apply(ast.literal_eval)
        self.df["main_director"] = self.df["directors"].apply(
            lambda x: x[0] if isinstance(x, list) and len(x) > 0 else None
        )
        director_avg = (
            self.df.explode("directors").groupby("directors")["vote_average"].mean().to_dict()
        )
        global_avg = self.df["vote_average"].mean()
        self.df["director_avg_score"] = self.df["directors"].apply(
            lambda director_list: sum([director_avg.get(d, global_avg) for d in director_list]) / len(director_list)
            if director_list else global_avg
        )
        return self

    def create_cast_avg_score(self, top_n=5):
        self.df["cast"] = self.df["cast"].apply(ast.literal_eval)
        self.df["top_cast"] = self.df["cast"].apply(
            lambda x: x[:top_n] if isinstance(x, list) else []
        )
        actor_avg = (
            self.df.explode("top_cast")
                .groupby("top_cast")["vote_average"]
                .mean()
                .to_dict()
        )
        self.df["cast_avg_score"] = self.df["top_cast"].apply(
            lambda cast_list: sum([actor_avg.get(a, 0) for a in cast_list]) / len(cast_list)
            if cast_list else 0
        )
        return self

    def drop_after_feature_engineering(self):
        cols_to_drop = [
            "title",
            "genres",
            "release_date",
            "directors",
            "cast",
            "main_director",
            "top_cast"
        ]
        self.df.drop(columns=cols_to_drop, inplace=True, errors='ignore')
        return self


    def run_all(self):
        return (
            self.drop_unused_columns()
                .create_release_month()
                .create_monthly_avg_score()
                .create_genre_avg_score()
                .create_director_avg_score()
                .create_cast_avg_score()
                .drop_after_feature_engineering()
                .df
        )
        
    def save_processed_data(self, path="processed_movies.csv"):
        if self.df is None:
            raise ValueError("❌ DataFrame is empty. 먼저 run_all()을 실행하세요.")
        self.df.to_csv(path, index=False, encoding="utf-8-sig")
        print(f"✅ 데이터 저장 완료: {path}")
