from openai import OpenAI
from src.config import get_settings

settings = get_settings()
client = OpenAI(api_key=settings.openai_api_key)

def generate_embedding(text: str) -> list[float]:
    try:
        response = client.embeddings.create(
            input=text,
            model=settings.openai_embedding_model,
            encoding_format="float"
        )
        return response.data[0].embedding
    except Exception as e:
        print(f"Error generating embedding: {e}")
        return []
    
def generate_embeddings_batch(texts: list[str]) -> list[list[float]]:
    try:
        response = client.embeddings.create(
            input=texts,
            model=settings.openai_embedding_model,
            encoding_format="float"
        )
        return [d.embedding for d in response.data]
    except Exception as e:
        print(f"Error generating batch embeddings: {e}")
        return [[] for _ in texts]

def generate_response(prompt: str) -> str:
    try:
        response = client.chat.completions.create(
            model=settings.openai_model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant that answers questions based on the provided context."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        raise Exception(f"LLM error: {str(e)}")