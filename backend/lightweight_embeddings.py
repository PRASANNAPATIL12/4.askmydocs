import numpy as np
import os
from typing import List, Dict, Any
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import hashlib

class LightweightEmbeddings:
    def __init__(self):
        self.tfidf_vectorizer = None
        self.global_vocabulary = set()
        self.is_fitted = False
        self.document_embeddings_cache = {}
        self.all_processed_texts = []  # Store all texts for consistent vectorizer fitting
    
    def _get_or_create_vectorizer(self, texts: List[str] = None) -> TfidfVectorizer:
        """Create or get a TF-IDF vectorizer fitted on all processed texts"""
        if texts:
            self.all_processed_texts.extend(texts)
        
        # Always create a fresh vectorizer fitted on all texts
        if self.all_processed_texts:
            self.tfidf_vectorizer = TfidfVectorizer(
                stop_words='english',
                ngram_range=(1, 2),  # Include bigrams for better context
                lowercase=True,
                max_features=1000,  # Fixed dimension
                min_df=1,  # Include even single occurrence words
                max_df=0.95  # Exclude very common words
            )
            
            # Fit on all processed texts to maintain consistency
            self.tfidf_vectorizer.fit(self.all_processed_texts)
            self.is_fitted = True
        
        return self.tfidf_vectorizer
    
    def get_embeddings_tfidf(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings using TF-IDF with consistent dimensions"""
        try:
            if not texts:
                return []
            
            # Get or create vectorizer with current texts
            vectorizer = self._get_or_create_vectorizer(texts)
            
            if not vectorizer or not self.is_fitted:
                print("Warning: Vectorizer not fitted, using fallback")
                return self._simple_word_embeddings(texts)
            
            # Transform texts to TF-IDF vectors
            tfidf_matrix = vectorizer.transform(texts)
            embeddings = tfidf_matrix.toarray().tolist()
            
            print(f"✅ Generated {len(embeddings)} embeddings with dimension {len(embeddings[0]) if embeddings else 0}")
            
            return embeddings
            
        except Exception as e:
            print(f"❌ TF-IDF embedding error: {e}")
            # Fallback to simple word embeddings
            return self._simple_word_embeddings(texts)
    
    def _simple_word_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Fallback: Simple word-based embeddings with fixed dimensions"""
        # Create a fixed vocabulary from all texts
        all_words = set()
        for text in texts:
            words = text.lower().split()
            all_words.update(words)
        
        # Use top 1000 words for consistency
        word_list = sorted(list(all_words))[:1000]
        
        # Pad to exactly 1000 dimensions
        while len(word_list) < 1000:
            word_list.append(f"pad_{len(word_list)}")
        
        embeddings = []
        for text in texts:
            words = set(text.lower().split())
            embedding = [1.0 if word in words else 0.0 for word in word_list]
            embeddings.append(embedding)
        
        return embeddings
    
    def get_query_embedding(self, query: str) -> List[float]:
        """Get embedding for a single query with consistent dimensions"""
        try:
            if self.tfidf_vectorizer is None or not self.is_fitted:
                print("Warning: No fitted vectorizer available for query")
                return self._simple_word_embeddings([query])[0]
            
            # Transform query using existing vectorizer
            query_vector = self.tfidf_vectorizer.transform([query])
            embedding = query_vector.toarray()[0].tolist()
            
            print(f"✅ Generated query embedding with dimension {len(embedding)}")
            
            return embedding
            
        except Exception as e:
            print(f"❌ Error generating query embedding: {e}")
            return self._simple_word_embeddings([query])[0]
    
    def find_relevant_chunks(self, query: str, document_chunks: List[str], 
                           document_embeddings: List[List[float]], top_k: int = 3) -> List[dict]:
        """Find most relevant chunks using cosine similarity with robust error handling"""
        try:
            if not document_chunks or not document_embeddings:
                print("❌ No document chunks or embeddings provided")
                return []
            
            # Get query embedding
            query_embedding = self.get_query_embedding(query)
            
            if not query_embedding or all(x == 0 for x in query_embedding):
                print("❌ Failed to generate query embedding, using keyword search")
                return self._simple_keyword_search(query, document_chunks, top_k)
            
            # Ensure dimensions match
            query_dim = len(query_embedding)
            
            # Calculate cosine similarities
            similarities = []
            query_embedding_np = np.array(query_embedding).reshape(1, -1)
            
            for i, doc_emb in enumerate(document_embeddings):
                try:
                    # Ensure same dimensions
                    if len(doc_emb) != query_dim:
                        print(f"⚠️ Dimension mismatch: query={query_dim}, doc={len(doc_emb)}")
                        # Use keyword search as fallback for this document
                        continue
                    
                    doc_emb_np = np.array(doc_emb).reshape(1, -1)
                    
                    # Handle zero vectors
                    if np.all(query_embedding_np == 0) or np.all(doc_emb_np == 0):
                        similarity = 0.0
                    else:
                        similarity = cosine_similarity(query_embedding_np, doc_emb_np)[0][0]
                    
                    similarities.append((i, similarity))
                    
                except Exception as e:
                    print(f"❌ Error computing similarity for chunk {i}: {e}")
                    continue
            
            if not similarities:
                print("❌ No valid similarities computed, using keyword search")
                return self._simple_keyword_search(query, document_chunks, top_k)
            
            # Sort by similarity and take top k
            similarities.sort(key=lambda x: x[1], reverse=True)
            
            results = []
            for idx, sim_score in similarities[:top_k]:
                if sim_score > 0.05:  # Lower threshold for better recall
                    results.append({
                        'chunk_index': int(idx),
                        'content': document_chunks[idx],
                        'relevance_score': float(sim_score)
                    })
            
            print(f"✅ Found {len(results)} relevant chunks with scores: {[r['relevance_score'] for r in results]}")
            
            # If no results from embedding search, try keyword search
            if not results:
                print("❌ No relevant chunks found with embeddings, trying keyword search")
                return self._simple_keyword_search(query, document_chunks, top_k)
            
            return results
            
        except Exception as e:
            print(f"❌ Error in relevance search: {e}")
            # Fallback to simple keyword matching
            return self._simple_keyword_search(query, document_chunks, top_k)
    
    def _simple_keyword_search(self, query: str, chunks: List[str], top_k: int = 3) -> List[dict]:
        """Fallback: Simple keyword-based search"""
        try:
            query_words = set(query.lower().split())
            
            chunk_scores = []
            for i, chunk in enumerate(chunks):
                chunk_words = set(chunk.lower().split())
                score = len(query_words.intersection(chunk_words)) / len(query_words) if query_words else 0
                chunk_scores.append((i, score))
            
            # Sort by score and take top k
            chunk_scores.sort(key=lambda x: x[1], reverse=True)
            
            results = []
            for idx, score in chunk_scores[:top_k]:
                if score > 0:
                    results.append({
                        'chunk_index': idx,
                        'content': chunks[idx],
                        'relevance_score': score
                    })
            
            return results
            
        except Exception as e:
            print(f"Error in keyword search: {e}")
            return []

# Global embeddings instance
embeddings_engine = LightweightEmbeddings()