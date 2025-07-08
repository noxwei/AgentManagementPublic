#!/usr/bin/env python3
"""
🧠 Hybrid Personality Loader
============================

Loads agent personalities from both PostgreSQL and JSON sources.
Provides unified interface for agent personality data.

Public release version - sanitized for open source distribution.
"""

import os
import json
import psycopg2
import psycopg2.extras
from pathlib import Path
from datetime import datetime

class HybridPersonalityLoader:
    """Load agent personalities from hybrid storage"""
    
    def __init__(self, config_path=None, json_dir=None):
        """
        Initialize with configurable paths for different environments
        
        Args:
            config_path: Path to database configuration file
            json_dir: Directory containing JSON personality files
        """
        self.db_config = self._load_db_config(config_path)
        self.json_dir = Path(json_dir or "./personalities")
        self.json_dir.mkdir(exist_ok=True)
    
    def _load_db_config(self, config_path):
        """Load database configuration from file or environment"""
        if config_path and Path(config_path).exists():
            with open(config_path, 'r') as f:
                return json.load(f)
        
        return {
            'host': os.getenv('DB_HOST', 'localhost'),
            'database': os.getenv('DB_NAME', 'agent_system'),
            'user': os.getenv('DB_USER', 'agent_user'),
            'password': os.getenv('DB_PASSWORD', ''),
            'port': int(os.getenv('DB_PORT', 5432))
        }
    
    def load_agent_personality(self, agent_name: str):
        """Load complete agent personality from hybrid sources"""
        
        # 1. Load core personality from PostgreSQL
        core_personality = self.load_core_personality(agent_name)
        
        # 2. Load detailed personality from JSON
        detailed_personality = self.load_detailed_personality(agent_name)
        
        # 3. Load relationships from PostgreSQL
        relationships = self.load_agent_relationships(agent_name)
        
        # 4. Merge into complete personality
        return self.merge_personality_layers(core_personality, detailed_personality, relationships)
    
    def load_core_personality(self, agent_name: str):
        """Load core personality from PostgreSQL"""
        try:
            with psycopg2.connect(**self.db_config) as conn:
                with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                    cur.execute("""
                        SELECT * FROM agent_personality_overview 
                        WHERE agent_name = %s
                    """, (agent_name,))
                    
                    result = cur.fetchone()
                    return dict(result) if result else {}
        except Exception as e:
            print(f"Failed to load core personality for {agent_name}: {e}")
            return {}
    
    def load_detailed_personality(self, agent_name: str):
        """Load detailed personality from JSON"""
        json_file = self.json_dir / f"{agent_name}_personality.json"
        
        try:
            if json_file.exists():
                with open(json_file, 'r') as f:
                    return json.load(f)
            else:
                return {"detailed_traits": {}, "response_patterns": {}}
        except Exception as e:
            print(f"Failed to load detailed personality for {agent_name}: {e}")
            return {"detailed_traits": {}, "response_patterns": {}}
    
    def load_agent_relationships(self, agent_name: str):
        """Load agent relationships from PostgreSQL"""
        try:
            with psycopg2.connect(**self.db_config) as conn:
                with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                    cur.execute("""
                        SELECT * FROM agent_relationship_network 
                        WHERE agent_1 = %s OR agent_2 = %s
                    """, (agent_name, agent_name))
                    
                    return [dict(row) for row in cur.fetchall()]
        except Exception as e:
            print(f"Failed to load relationships for {agent_name}: {e}")
            return []
    
    def merge_personality_layers(self, core, detailed, relationships):
        """Merge personality layers into unified structure"""
        return {
            "core_personality": core,
            "detailed_traits": detailed.get("detailed_traits", {}),
            "response_patterns": detailed.get("response_patterns", {}),
            "relationships": relationships,
            "learning_history": detailed.get("learning_history", []),
            "contextual_memories": detailed.get("contextual_memories", []),
            "loaded_at": datetime.now().isoformat()
        }
    
    def update_personality_component(self, agent_name: str, component: str, data: dict):
        """Update specific personality component"""
        if component == "core":
            return self.update_core_personality(agent_name, data)
        elif component == "detailed":
            return self.update_detailed_personality(agent_name, data)
        elif component == "relationships":
            return self.update_relationships(agent_name, data)
    
    def update_core_personality(self, agent_name: str, data: dict):
        """Update core personality in PostgreSQL"""
        try:
            with psycopg2.connect(**self.db_config) as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        UPDATE agent_personalities 
                        SET personality_type = %s, communication_style = %s, 
                            authority_level = %s, cultural_background = %s,
                            management_philosophy = %s, activity_level = %s,
                            updated_at = NOW()
                        WHERE agent_id = (SELECT agent_id FROM agents WHERE agent_name = %s)
                    """, (
                        data.get("personality_type"),
                        data.get("communication_style"),
                        data.get("authority_level"),
                        data.get("cultural_background"),
                        data.get("management_philosophy"),
                        data.get("activity_level"),
                        agent_name
                    ))
                    conn.commit()
                    return True
        except Exception as e:
            print(f"Failed to update core personality for {agent_name}: {e}")
            return False
    
    def update_detailed_personality(self, agent_name: str, data: dict):
        """Update detailed personality in JSON"""
        json_file = self.json_dir / f"{agent_name}_personality.json"
        
        try:
            # Load existing
            existing = {}
            if json_file.exists():
                with open(json_file, 'r') as f:
                    existing = json.load(f)
            
            # Update with new data
            existing.update(data)
            
            # Save back
            with open(json_file, 'w') as f:
                json.dump(existing, f, indent=2)
            
            return True
        except Exception as e:
            print(f"Failed to update detailed personality for {agent_name}: {e}")
            return False

# Example usage
if __name__ == "__main__":
    # Initialize loader
    loader = HybridPersonalityLoader()
    
    # Test loading a personality
    personality = loader.load_agent_personality("example_agent")
    print(json.dumps(personality, indent=2))