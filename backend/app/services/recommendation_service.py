from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

class RecommendationService:
    def __init__(self):
        # This is a very basic example. In a real system, you'd use embeddings
        # from models like Sentence Transformers or OpenAI embeddings.
        self.items = [
            {"id": 1, "name": "Laptop", "description": "Powerful laptop for work and gaming.", "category": "electronics"},
            {"id": 2, "name": "Smartphone", "description": "Latest smartphone with advanced camera.", "category": "electronics"},
            {"id": 3, "name": "Headphones", "description": "Noise-cancelling headphones for immersive audio.", "category": "accessories"},
            {"id": 4, "name": "Desk Chair", "description": "Ergonomic chair for comfortable working.", "category": "furniture"},
            {"id": 5, "name": "Monitor", "description": "High-resolution monitor for productivity.", "category": "electronics"},
        ]
        self.vectorizer = TfidfVectorizer()
        self.item_vectors = self.vectorizer.fit_transform([item["description"] for item in self.items])

    async def get_recommendations(self, query: str, top_k: int = 3) -> list[str]:
        if not query:
            return [item["name"] for item in self.items[:top_k]] # Return some default items

        try:
            query_vector = self.vectorizer.transform([query])
            similarities = cosine_similarity(query_vector, self.item_vectors).flatten()
            
            # Get top_k indices of most similar items
            top_indices = similarities.argsort()[-top_k:][::-1]
            
            recommendations = [self.items[i]["name"] for i in top_indices]
            return recommendations
        except Exception as e:
            print(f"Error generating recommendations: {e}")
            return []
