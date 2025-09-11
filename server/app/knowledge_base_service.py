import os
import re
import random
from typing import List, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from config_loader import config

class KnowledgeBaseService:
    def __init__(self, kb_name: str = None):
        self.kb_name = kb_name
        self.qa_pairs = []
        
        # Load configuration
        kb_config = config.get_knowledge_base_config()
        tfidf_settings = kb_config.get('tfidf_settings', {})
        
        self.vectorizer = TfidfVectorizer(
            stop_words=tfidf_settings.get('stop_words'),
            lowercase=tfidf_settings.get('lowercase', True), 
            max_features=tfidf_settings.get('max_features', 1000)
        )
        self.tfidf_matrix = None
        self.similarity_threshold = config.get_similarity_threshold()
        self.load_knowledge_base()

    def load_knowledge_base(self):
        """Load knowledge base file and parse Q&A pairs"""
        kb_file = config.get_knowledge_base_path(self.kb_name)
        
        if not os.path.exists(kb_file):
            print(f"Knowledge base file not found: {kb_file}")
            return
            
        with open(kb_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Parse Q&A pairs - supports both markdown and plain text formats
        # Try plain text format first (Q: ... A: ...)
        qa_pattern_plain = r'Q:\s*(.*?)\n\s*A:\s*(.*?)(?=\n\n|\nQ:|$)'
        matches = re.findall(qa_pattern_plain, content, re.DOTALL)
        
        # If no matches with plain text, try markdown format (**Q: ... **A: ...)
        if not matches:
            qa_pattern_markdown = r'\*\*Q:\s*(.*?)\*\*\s*\n\s*A:\s*(.*?)(?=\n\n|\n\*\*Q:|$)'
            matches = re.findall(qa_pattern_markdown, content, re.DOTALL)
        
        self.qa_pairs = []
        for question, answer in matches:
            self.qa_pairs.append({
                'question': question.strip(),
                'answer': answer.strip()
            })
        
        print(f"Loaded {len(self.qa_pairs)} Q&A pairs from knowledge base: {kb_file}")
        
        # Build TF-IDF vectors
        if self.qa_pairs:
            questions = [qa['question'] for qa in self.qa_pairs]
            self.tfidf_matrix = self.vectorizer.fit_transform(questions)

    def search_knowledge_base(self, query: str, threshold: float = None) -> Tuple[str, bool, float]:
        """
        Search for relevant answers in knowledge base
        Returns: (answer, found_match, similarity_score)
        """
        if threshold is None:
            threshold = self.similarity_threshold
            
        if not self.qa_pairs or self.tfidf_matrix is None:
            no_match_responses = config.get_no_match_responses()
            return random.choice(no_match_responses), False, 0.0
        
        # Calculate similarity between query and all questions
        query_vector = self.vectorizer.transform([query])
        similarities = cosine_similarity(query_vector, self.tfidf_matrix)[0]
        
        # Find most similar question
        best_match_idx = np.argmax(similarities)
        best_similarity = similarities[best_match_idx]
        
        if best_similarity >= threshold:
            answer = self.qa_pairs[best_match_idx]['answer']
            return answer, True, best_similarity
        else:
            no_match_responses = config.get_no_match_responses()
            return random.choice(no_match_responses), False, best_similarity

    def detect_kb_topic(self) -> str:
        """Detect the main topic/domain of the loaded knowledge base"""
        if not self.qa_pairs:
            return "general"
        
        # Analyze questions to determine topic
        all_text = " ".join([qa['question'] + " " + qa['answer'] for qa in self.qa_pairs]).lower()
        
        # Topic detection based on keyword frequency
        topic_keywords = {
            'automotive': ['car', 'vehicle', 'auto', 'insurance', 'buy', 'sell', 'drive', 'engine', 'repair'],
            'technology': ['software', 'computer', 'app', 'system', 'code', 'programming', 'tech', 'device'],
            'finance': ['money', 'bank', 'loan', 'credit', 'payment', 'investment', 'financial', 'account'],
            'health': ['health', 'medical', 'doctor', 'medicine', 'symptom', 'treatment', 'patient', 'hospital'],
            'education': ['school', 'student', 'learn', 'course', 'study', 'education', 'teacher', 'class'],
            'ecommerce': ['product', 'order', 'shipping', 'return', 'purchase', 'customer', 'delivery', 'store']
        }
        
        topic_scores = {}
        for topic, keywords in topic_keywords.items():
            score = sum(all_text.count(keyword) for keyword in keywords)
            if score > 0:
                topic_scores[topic] = score
        
        if topic_scores:
            return max(topic_scores, key=topic_scores.get)
        return "general"

    def get_all_qa_pairs(self) -> List[dict]:
        """Get all Q&A pairs"""
        return self.qa_pairs

    def add_qa_pair(self, question: str, answer: str):
        """Add new Q&A pair (can be used for dynamic knowledge base updates)"""
        self.qa_pairs.append({
            'question': question,
            'answer': answer
        })
        # Rebuild TF-IDF vectors
        questions = [qa['question'] for qa in self.qa_pairs]
        self.tfidf_matrix = self.vectorizer.fit_transform(questions)
    
    def switch_knowledge_base(self, kb_name: str):
        """Switch to a different knowledge base"""
        self.kb_name = kb_name
        self.load_knowledge_base()
    
    def get_available_knowledge_bases(self) -> List[str]:
        """Get list of available knowledge bases"""
        kb_config = config.get_knowledge_base_config()
        return list(kb_config.get('available_kbs', {}).keys())
    
    def reload_config(self):
        """Reload configuration and knowledge base"""
        config.reload_configs()
        self.similarity_threshold = config.get_similarity_threshold()
        self.load_knowledge_base()