from src.vector_dataframe import VectorDataframe
from src.retriever import Retriever
from src.generator import Generator

class RAGWare:
    def __init__(self, vector_df: VectorDataframe):
        self.retriever = Retriever(vector_df)
        self.generator = Generator()
        
    def query(self, user_query: str, top_k: int = 3, return_context: bool = False):
        relevant_chunks = self.retriever.retrieve(user_query, top_k=top_k)
        response = self.generator.generate(user_query, context_chunks=relevant_chunks)
        
        result = {"response": response, "context": None}
        if return_context:
            result["context"] = relevant_chunks[['chunked_combined', 'similarity']]
        return result
    
if __name__ == "__main__":
    vdf = VectorDataframe()
    ragware = RAGWare(vdf)
    user_query = "What time of day do people buy the most coffee?"
    result = ragware.query(user_query, top_k=5, return_context=True)
    print(result)