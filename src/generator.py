import pandas as pd
from src.llm_service import generate_response

class Generator:
    def generate(self, query: str, context_chunks: pd.DataFrame) -> str:
        context = self._build_context(context_chunks)
        prompt = self._build_prompt(query, context)
        return generate_response(prompt)

    def _build_context(self, chunks: pd.DataFrame) -> str:
        context_parts = []
        for idx, row in chunks.iterrows():
            context_parts.append(f"[Chunk {idx}] {row['chunked_combined']}")
        return "\n\n".join(context_parts)
    
    def _build_prompt(self, query: str, context: str) -> str:
        return f"""Based on the following context, please answer the question.
                Context:
                {context}
                Question: {query}"""
                
if __name__ == "__main__":
    from src.retriever import Retriever
    from src.vector_dataframe import VectorDataframe
    
    vdf = VectorDataframe()
    retriever = Retriever(vdf)
    generator = Generator()
    
    user_query = "What time of day do people buy the most coffee?"
    chunks = retriever.retrieve(user_query)
    print(chunks)
    print(generator.generate(user_query, chunks))