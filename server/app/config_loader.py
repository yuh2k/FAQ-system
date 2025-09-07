import yaml
import os
from typing import Dict, Any, List
from pathlib import Path

class ConfigLoader:
    def __init__(self, config_dir: str = None):
        if config_dir is None:
            # Default to config directory relative to this file
            self.config_dir = Path(__file__).parent.parent / "config"
        else:
            self.config_dir = Path(config_dir)
        
        self.kb_config = None
        self.ai_config = None
        self._load_configs()
    
    def _load_configs(self):
        """Load all configuration files"""
        try:
            # Load knowledge base config
            kb_config_path = self.config_dir / "knowledge_base_config.yaml"
            with open(kb_config_path, 'r', encoding='utf-8') as f:
                self.kb_config = yaml.safe_load(f)
            
            # Load AI prompts config
            ai_config_path = self.config_dir / "ai_prompts_config.yaml"
            with open(ai_config_path, 'r', encoding='utf-8') as f:
                self.ai_config = yaml.safe_load(f)
                
        except Exception as e:
            print(f"Error loading configs: {e}")
            raise
    
    def get_knowledge_base_config(self) -> Dict[str, Any]:
        """Get knowledge base configuration"""
        return self.kb_config.get('knowledge_base', {})
    
    def get_topic_config(self, topic: str = 'automotive') -> Dict[str, Any]:
        """Get topic-specific configuration"""
        return self.kb_config.get('topics', {}).get(topic, {})
    
    def get_ai_prompts(self) -> Dict[str, Any]:
        """Get AI prompts configuration"""
        return self.ai_config.get('ai_prompts', {})
    
    def get_response_templates(self) -> Dict[str, Any]:
        """Get response templates"""
        return self.ai_config.get('response_templates', {})
    
    def get_ai_settings(self) -> Dict[str, Any]:
        """Get AI model settings"""
        return self.ai_config.get('ai_settings', {})
    
    def get_ticket_logic(self) -> Dict[str, Any]:
        """Get ticket creation logic configuration"""
        return self.ai_config.get('ticket_logic', {})
    
    def get_knowledge_base_path(self, kb_name: str = None) -> str:
        """Get path to knowledge base file"""
        kb_config = self.get_knowledge_base_config()
        
        if kb_name is None:
            # Use primary KB
            kb_file = kb_config.get('primary_kb_file', 'knowledge_bases/automotive_en.txt')
        else:
            # Use specific KB
            available_kbs = kb_config.get('available_kbs', {})
            kb_file = available_kbs.get(kb_name, 'knowledge_bases/automotive_en.txt')
        
        return str(self.config_dir / kb_file)
    
    def get_urgent_keywords(self, topic: str = 'automotive') -> List[str]:
        """Get urgent keywords for a topic"""
        topic_config = self.get_topic_config(topic)
        return topic_config.get('urgent_keywords', [])
    
    def get_similarity_threshold(self) -> float:
        """Get similarity threshold for knowledge base search"""
        kb_config = self.get_knowledge_base_config()
        return kb_config.get('similarity_threshold', 0.3)
    
    def get_no_match_responses(self) -> List[str]:
        """Get fallback responses when no match found"""
        kb_config = self.get_knowledge_base_config()
        return kb_config.get('no_match_responses', [
            "I couldn't find a relevant answer in the knowledge base. Please contact customer service."
        ])
    
    def reload_configs(self):
        """Reload configuration files"""
        self._load_configs()

# Global config instance
config = ConfigLoader()