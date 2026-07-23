from app.services.embedding_service import EmbeddingService

service = EmbeddingService()

embeddings = service.get_embeddings()

print(type(embeddings))

vector = embeddings.embed_query("How do I restart the server?")

print(len(vector))