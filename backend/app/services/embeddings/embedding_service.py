import numpy as np
from typing import List, Optional
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from app.core.config import settings
from app.core.logging import logger

try:
    from google import genai
except ImportError:
    genai = None


class EmbeddingService:
    """Generates 768-dimensional embeddings via Google Gemini Embedding 2 with automatic TF-IDF fallback."""

    def __init__(self):
        self.api_key = settings.GEMINI_API_KEY
        self.model_name = settings.GEMINI_EMBEDDING_MODEL
        self.dimension = settings.EMBEDDING_DIMENSION
        self.client = None
        if self.api_key and genai:
            try:
                self.client = genai.Client(api_key=self.api_key)
            except Exception as e:
                logger.warning(f"Could not initialize Google GenAI Client: {e}")

    async def get_embedding(self, text: str) -> List[float]:
        """Gets embedding vector from Gemini or returns deterministic TF-IDF representation."""
        if not text or not text.strip():
            return [0.0] * self.dimension

        if self.client:
            try:
                # Use Google GenAI SDK
                response = self.client.models.embed_content(
                    model=self.model_name,
                    contents=text[:2000]
                )
                if response and hasattr(response, "embedding") and response.embedding:
                    vec = list(response.embedding.values)
                    # Ensure correct dimension
                    if len(vec) == self.dimension:
                        return vec
                    elif len(vec) > self.dimension:
                        return vec[:self.dimension]
                    else:
                        return vec + [0.0] * (self.dimension - len(vec))
            except Exception as e:
                logger.warning(f"Gemini embedding API call failed: {e}. Falling back to deterministic vector.")

        # Deterministic pseudo-embedding for fallback
        return self._generate_fallback_vector(text)

    def _generate_fallback_vector(self, text: str) -> List[float]:
        """Generates a stable deterministic 768-dim float vector from text hash and terms."""
        import hashlib
        words = text.lower().split()
        vec = np.zeros(self.dimension, dtype=np.float32)
        for i, word in enumerate(words[:150]):
            h = int(hashlib.md5(word.encode("utf-8")).hexdigest(), 16)
            idx = h % self.dimension
            val = (h % 1000) / 1000.0
            vec[idx] += val

        norm = np.linalg.norm(vec)
        if norm > 0:
            vec = vec / norm
        return vec.tolist()

    def calculate_similarity(self, vec1: Optional[List[float]], vec2: Optional[List[float]], text1: str = "", text2: str = "") -> float:
        """Calculates cosine similarity between two vectors or falls back to direct TF-IDF on texts."""
        if vec1 and vec2 and len(vec1) == len(vec2):
            v1 = np.array(vec1, dtype=np.float32)
            v2 = np.array(vec2, dtype=np.float32)
            norm1 = np.linalg.norm(v1)
            norm2 = np.linalg.norm(v2)
            if norm1 > 0 and norm2 > 0:
                sim = float(np.dot(v1, v2) / (norm1 * norm2))
                return max(0.0, min(1.0, sim))

        # Direct TF-IDF text similarity fallback
        if text1 and text2:
            try:
                tfidf = TfidfVectorizer(stop_words="english", max_features=1000)
                matrix = tfidf.fit_transform([text1, text2])
                sim = float(cosine_similarity(matrix[0:1], matrix[1:2])[0][0])
                return max(0.0, min(1.0, sim))
            except Exception:
                pass

        return 0.5


embedding_service = EmbeddingService()
