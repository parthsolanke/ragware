import numpy as np
import pandas as pd
from src.llm_service import generate_embedding
from src.vector_dataframe import VectorDataframe

class Retriever:
    def __init__(self, vector_df: VectorDataframe):
        self.vdf = vector_df
        self._convert_string_embeddings_to_numpy_arrays()
        
    def retrieve(self, query: str, top_k: int = 3) -> pd.DataFrame:
        query_embedding = np.array(generate_embedding(query))
        similarities = self._cosine_similarity(query_embedding, self.embeddings_matrix)
        top_indices = np.argsort(similarities)[-top_k:][::-1]
        results = self.vdf.df.iloc[top_indices].copy()
        results['similarity'] = similarities[top_indices]
        return results
    
    def _cosine_similarity(self, query_vec: np.ndarray, doc_matrix: np.ndarray) -> np.ndarray:
        query_norm = query_vec / np.linalg.norm(query_vec)
        doc_norms = doc_matrix / np.linalg.norm(doc_matrix, axis=1, keepdims=True)
        similarities = np.dot(doc_norms, query_norm)
        return similarities
    
    def _convert_string_embeddings_to_numpy_arrays(self):
        if isinstance(self.vdf.df['embedding'].iloc[0], str):
            self.vdf.df['embedding'] = self.vdf.df['embedding'].apply(eval)
        self.embeddings_matrix = np.array(self.vdf.df['embedding'].tolist())
        
if __name__ == "__main__":
    vdf = VectorDataframe()
    retriever = Retriever(vdf)
    print(retriever.retrieve("Americano Coffee"))