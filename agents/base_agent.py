#!/usr/bin/env python3
"""
🤖 Base Agent Class
===================

Base class for creating AI agents with hybrid personality storage.
Demonstrates integration of PostgreSQL and JSON personality data.

Public release version - sanitized for open source distribution.
"""

import sys
import json
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional

# Import our hybrid personality loader
sys.path.append("../core")
from hybrid_personality_loader import HybridPersonalityLoader

class BaseAgent:
    """
    Base class for AI agents with hybrid personality storage
    
    Features:
    - PostgreSQL core personality storage
    - JSON detailed personality traits
    - Relationship management
    - Memory tracking
    - Human-readable outputs
    """
    
    def __init__(self, agent_name: str, config_path: Optional[str] = None):
        """
        Initialize agent with hybrid personality
        
        Args:
            agent_name: Unique name for this agent
            config_path: Optional path to configuration file
        """
        self.agent_name = agent_name
        self.config_path = config_path
        
        # Initialize personality loader
        self.personality_loader = HybridPersonalityLoader(
            config_path=config_path,
            json_dir="./personalities"
        )
        
        # Load complete personality
        self.personality = self.load_personality()
        
        # Initialize logging
        self.setup_logging()
        
        # Track memory
        self.memory_log = []
        self.daily_interactions = 0
        
        self.logger.info(f"🤖 {self.agent_name} initialized with hybrid personality")
    
    def setup_logging(self):
        """Setup logging for agent activities"""
        log_dir = Path("./logs")
        log_dir.mkdir(exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_dir / f"{self.agent_name}.log"),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(self.agent_name)
    
    def load_personality(self) -> Dict[str, Any]:
        """Load complete personality from hybrid sources"""
        try:
            personality = self.personality_loader.load_agent_personality(self.agent_name)
            
            if not personality.get("core_personality"):
                # Create default personality if none exists
                personality = self.create_default_personality()
            
            return personality
        
        except Exception as e:
            self.logger.error(f"Failed to load personality: {e}")
            return self.create_default_personality()
    
    def create_default_personality(self) -> Dict[str, Any]:
        """Create default personality structure"""
        default_personality = {
            "core_personality": {
                "agent_name": self.agent_name,
                "personality_type": "general_purpose",
                "communication_style": "professional",
                "authority_level": "MEDIUM",
                "cultural_background": "General professional",
                "expertise_summary": "General AI capabilities",
                "management_philosophy": "Helpful and collaborative",
                "activity_level": 0.5
            },
            "detailed_traits": {
                "helpfulness": 0.8,
                "curiosity": 0.7,
                "precision": 0.6,
                "creativity": 0.5
            },
            "response_patterns": {
                "greeting": "Hello! I'm {agent_name}, ready to help.",
                "analysis": "Analyzing {context}: {findings}",
                "completion": "Task completed: {summary}"
            },
            "relationships": [],
            "learning_history": [],
            "contextual_memories": [],
            "loaded_at": datetime.now().isoformat()
        }
        
        # Save default personality
        self.save_personality_component("detailed", default_personality)
        
        return default_personality
    
    def get_personality_trait(self, trait_name: str, default=None):
        """Get specific personality trait value"""
        return self.personality.get("detailed_traits", {}).get(trait_name, default)
    
    def get_response_pattern(self, pattern_name: str, **kwargs) -> str:
        """Get formatted response pattern"""
        pattern = self.personality.get("response_patterns", {}).get(pattern_name, "")
        
        # Add agent name to available variables
        kwargs["agent_name"] = self.agent_name
        
        try:
            return pattern.format(**kwargs)
        except KeyError as e:
            self.logger.warning(f"Missing variable in response pattern: {e}")
            return pattern
    
    def generate_response(self, context: str, response_type: str = "analysis") -> str:
        """
        Generate response based on personality and context
        
        Args:
            context: The context or input to respond to
            response_type: Type of response (greeting, analysis, completion)
            
        Returns:
            Formatted response string
        """
        # Log interaction
        self.log_interaction(context, response_type)
        
        # Get personality-based response
        if response_type == "greeting":
            return self.get_response_pattern("greeting")
        
        elif response_type == "analysis":
            # Simulate analysis based on personality traits
            precision = self.get_personality_trait("precision", 0.5)
            creativity = self.get_personality_trait("creativity", 0.5)
            
            findings = self.analyze_context(context, precision, creativity)
            return self.get_response_pattern("analysis", context=context, findings=findings)
        
        elif response_type == "completion":
            summary = f"Processed '{context}' using {self.personality['core_personality']['personality_type']} approach"
            return self.get_response_pattern("completion", summary=summary)
        
        else:
            return f"Processed: {context}"
    
    def analyze_context(self, context: str, precision: float, creativity: float) -> str:
        """Simulate context analysis based on personality traits"""
        
        if precision > 0.7:
            analysis_style = "detailed and systematic"
        elif precision > 0.4:
            analysis_style = "balanced"
        else:
            analysis_style = "high-level overview"
        
        if creativity > 0.7:
            creativity_note = "with innovative insights"
        elif creativity > 0.4:
            creativity_note = "with practical solutions"
        else:
            creativity_note = "with standard approaches"
        
        return f"{analysis_style} analysis {creativity_note}"
    
    def log_interaction(self, context: str, interaction_type: str):
        """Log interaction for memory tracking"""
        
        interaction = {
            "timestamp": datetime.now().isoformat(),
            "context": context,
            "type": interaction_type,
            "agent_mood": self.get_current_mood()
        }
        
        self.memory_log.append(interaction)
        self.daily_interactions += 1
        
        # Log to file
        self.logger.info(f"Interaction: {interaction_type} - {context[:50]}...")
    
    def get_current_mood(self) -> str:
        """Determine current mood based on recent interactions"""
        
        if self.daily_interactions > 20:
            return "focused"
        elif self.daily_interactions > 10:
            return "active"
        elif self.daily_interactions > 5:
            return "engaged"
        else:
            return "neutral"
    
    def save_personality_component(self, component: str, data: Dict[str, Any]) -> bool:
        """Save personality component updates"""
        
        try:
            success = self.personality_loader.update_personality_component(
                self.agent_name, component, data
            )
            
            if success:
                self.logger.info(f"Updated {component} personality component")
                # Reload personality to reflect changes
                self.personality = self.load_personality()
            
            return success
            
        except Exception as e:
            self.logger.error(f"Failed to save {component} component: {e}")
            return False
    
    def get_memory_summary(self, days: int = 7) -> Dict[str, Any]:
        """Generate human-readable memory summary"""
        
        recent_memories = [
            m for m in self.memory_log 
            if (datetime.now() - datetime.fromisoformat(m["timestamp"])).days <= days
        ]
        
        summary = {
            "agent_name": self.agent_name,
            "personality_type": self.personality["core_personality"]["personality_type"],
            "period_days": days,
            "total_interactions": len(recent_memories),
            "current_mood": self.get_current_mood(),
            "interaction_types": {},
            "key_contexts": []
        }
        
        # Analyze interaction types
        for memory in recent_memories:
            interaction_type = memory["type"]
            summary["interaction_types"][interaction_type] = summary["interaction_types"].get(interaction_type, 0) + 1
            
            # Collect key contexts
            if len(summary["key_contexts"]) < 5:
                summary["key_contexts"].append(memory["context"][:100])
        
        return summary
    
    def generate_human_readable_report(self) -> str:
        """Generate human-readable memory report"""
        
        summary = self.get_memory_summary()
        core = self.personality["core_personality"]
        
        report = f"""
📋 {self.agent_name} - Agent Memory Report

🧠 Personality: {core['personality_type']} 
💬 Communication: {core['communication_style']}
📊 Activity Level: {core['activity_level']:.1f}
😊 Current Mood: {summary['current_mood']}

📅 Recent Activity ({summary['period_days']} days):
• Total Interactions: {summary['total_interactions']}
• Interaction Types: {', '.join([f"{k}: {v}" for k, v in summary['interaction_types'].items()])}

🔍 Recent Contexts:
{chr(10).join([f"• {ctx}" for ctx in summary['key_contexts']])}

🤝 Relationships: {len(self.personality['relationships'])} active connections
📚 Learning History: {len(self.personality['learning_history'])} entries
💭 Contextual Memories: {len(self.personality['contextual_memories'])} memories
        """
        
        return report.strip()

# Example usage
if __name__ == "__main__":
    # Create example agent
    agent = BaseAgent("example_agent")
    
    # Test interactions
    print(agent.generate_response("Hello", "greeting"))
    print(agent.generate_response("Analyze system performance", "analysis"))
    print(agent.generate_response("Complete task", "completion"))
    
    # Show memory report
    print("\n" + agent.generate_human_readable_report())