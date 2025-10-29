import pandas as pd
import tiktoken
import os
from tqdm import tqdm
from src.llm_service import generate_embeddings_batch
from src.config import get_settings

settings = get_settings()

class VectorDataframe:
    def __init__(self, batch_size: int = 100, max_tokens_per_chunk: int = 500):
        self.table_name = "coffee_sales"
        self.batch_size = batch_size
        self.max_tokens = max_tokens_per_chunk
        self.df = self._load_or_build_dataframe()

    def _load_or_build_dataframe(self) -> pd.DataFrame:
        if os.path.exists(settings.output_csv):
            print(f"Loading existing embeddings from {settings.output_csv}")
            return pd.read_csv(settings.output_csv)
        else:
            print("No existing embeddings found. Generating new embeddings.")
            df = self._load_csv()
            df.to_csv(settings.output_csv, index=False)
            return df

    def _load_csv(self) -> pd.DataFrame:
        try:
            df = pd.read_csv(settings.input_csv).dropna().reset_index(drop=False)
            df.rename(columns={"index": "row_id"}, inplace=True)
            df["combined"] = df.apply(self._combine_row, axis=1)
            chunked_df = self._get_chunked_dataframe(df)
            chunked_df["embedding"] = self._generate_embeddings_in_batches(chunked_df["chunked_combined"].tolist())
            return chunked_df
        except Exception as e:
            print(f"Error loading CSV: {e}")
            return pd.DataFrame()

    def _combine_row(self, row: pd.Series) -> str:
        return ', '.join([f"{col}: {row[col]}" for col in row.index])
    
    def _get_chunked_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        chunked_rows = []
        for _, row in df.iterrows():
            chunks, tokens = self._chunk_text(row["combined"])
            for i, chunk in enumerate(chunks):
                chunked_rows.append({
                    **row.to_dict(),
                    "chunk_id": i,
                    "chunk_uid": f"{row['row_id']}_{i}",
                    "chunked_combined": chunk,
                    "n_tokens": len(tokens)
                })
        return pd.DataFrame(chunked_rows)

    def _chunk_text(self, text: str) -> list[str]:
        encoding = tiktoken.get_encoding(settings.tiktoken_tokenizer)
        tokens = encoding.encode(text)
        chunks = []
        for i in range(0, len(tokens), self.max_tokens):
            chunk = encoding.decode(tokens[i:i + self.max_tokens])
            chunks.append(chunk)
        return chunks, tokens

    def _generate_embeddings_in_batches(self, texts: list[str]) -> list[list[float]]:
        embeddings = []
        for i in tqdm(range(0, len(texts), self.batch_size), desc="Generating embeddings"):
            batch = texts[i:i + self.batch_size]
            batch = [str(t) for t in batch]
            batch_embeddings = generate_embeddings_batch(batch)
            embeddings.extend(batch_embeddings)
        return embeddings

if __name__ == "__main__":
    vdf = VectorDataframe()
    print(vdf.df[["chunk_id", "chunked_combined", "n_tokens"]].head())
