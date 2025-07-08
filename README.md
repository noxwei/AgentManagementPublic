# 🤖 Agent Management System

A comprehensive AI agent management framework with hybrid personality storage, combining the flexibility of JSON with the power of PostgreSQL for scalable, human-readable agent systems.

## ✨ Features

- **🧠 Hybrid Personality Storage**: PostgreSQL for structured data + JSON for flexible traits
- **👥 Relationship Management**: Track and manage inter-agent relationships
- **📚 Memory Systems**: Human-readable memory summaries and learning history
- **🔄 Real-time Updates**: Live personality evolution and adaptation
- **📊 Analytics**: Query agent behaviors, relationships, and performance
- **🛡️ Security**: ACID compliance and data integrity
- **🎯 Scalable**: Handles individual agents to large agent networks

## 🚀 Quick Start

### 1. Database Setup

```bash
# Install PostgreSQL (if not already installed)
brew install postgresql  # macOS
sudo apt-get install postgresql  # Ubuntu

# Create database
createdb agent_system

# Load schema
psql agent_system < database/hybrid_personality_schema.sql
```

### 2. Install Dependencies

```bash
pip install psycopg2-binary
```

### 3. Basic Usage

```python
from agents.base_agent import BaseAgent

# Create an agent
agent = BaseAgent("my_assistant")

# Interact with the agent
greeting = agent.generate_response("Hello!", "greeting")
analysis = agent.generate_response("Analyze this data", "analysis")

print(greeting)  # "Hello! I'm my_assistant, ready to help."
print(analysis)  # Personality-based analysis response

# View memory report
print(agent.generate_human_readable_report())
```

## 📁 Project Structure

```
AgentManagementPublic/
├── 📁 core/                   # Core system components
│   └── hybrid_personality_loader.py
├── 📁 agents/                 # Agent classes and implementations
│   └── base_agent.py
├── 📁 database/              # Database schemas and migrations
│   └── hybrid_personality_schema.sql
├── 📁 personalities/         # JSON personality definitions
│   ├── security_agent_personality.json
│   └── productivity_agent_personality.json
├── 📁 examples/              # Usage examples and demos
│   └── basic_usage.py
├── 📁 docs/                  # Documentation
└── 📁 tests/                 # Test suites
```

## 🧠 Personality System

### Core Personality (PostgreSQL)
Structured metadata stored in PostgreSQL for fast queries and relationships:

```sql
-- Query agents by personality type
SELECT agent_name, personality_type, communication_style 
FROM agent_personality_overview 
WHERE personality_type = 'security_focused';

-- Analyze relationship networks
SELECT agent_1, agent_2, relationship_strength 
FROM agent_relationship_network 
WHERE strength_score > 0.7;
```

### Detailed Traits (JSON)
Flexible personality traits stored in JSON files:

```json
{
  "detailed_traits": {
    "creativity": 0.8,
    "risk_tolerance": 0.3,
    "communication_style": "formal_friendly"
  },
  "response_patterns": {
    "greeting": "Hello! I'm {agent_name}, ready to assist.",
    "analysis": "Analyzing {context}: {findings}"
  },
  "learning_history": [...],
  "contextual_memories": [...]
}
```

## 👥 Agent Relationships

Track and manage relationships between agents:

```python
# Agents automatically build relationships
security_agent = BaseAgent("security_monitor")
qa_agent = BaseAgent("quality_checker")

# Relationships are tracked in PostgreSQL
# Query relationship strength
relationships = security_agent.personality_loader.load_agent_relationships("security_monitor")
```

## 📊 Human-Readable Memory

Generate natural language summaries of agent activities:

```python
# Get human-readable memory report
report = agent.generate_human_readable_report()
print(report)
```

```
📋 security_agent - Agent Memory Report

🧠 Personality: security_focused 
💬 Communication: formal_alert
📊 Activity Level: 0.8
😊 Current Mood: vigilant

📅 Recent Activity (7 days):
• Total Interactions: 45
• Interaction Types: analysis: 20, greeting: 5, completion: 20

🔍 Recent Contexts:
• Vulnerability scan of production systems
• Security audit of user permissions
• Threat assessment of new software deployment
```

## 🔧 Configuration

### Database Configuration

Create a `config.json` file:

```json
{
  "host": "localhost",
  "database": "agent_system",
  "user": "agent_user",
  "password": "your_password",
  "port": 5432
}
```

### Environment Variables

```bash
export DB_HOST=localhost
export DB_NAME=agent_system
export DB_USER=agent_user
export DB_PASSWORD=your_password
export DB_PORT=5432
```

## 📚 Examples

### Creating Specialized Agents

```python
# Security-focused agent
security_agent = BaseAgent("security_guard")
security_traits = {
    "detailed_traits": {
        "threat_detection": 0.95,
        "risk_assessment": 0.9,
        "response_urgency": 0.85
    },
    "response_patterns": {
        "threat_alert": "🚨 SECURITY ALERT: {threat_type} detected!",
        "all_clear": "✅ Security scan complete - No threats found"
    }
}
security_agent.save_personality_component("detailed", security_traits)

# Productivity optimization agent
productivity_agent = BaseAgent("efficiency_coach")
productivity_traits = {
    "detailed_traits": {
        "optimization_focus": 0.9,
        "encouragement_level": 0.8,
        "data_analysis": 0.85
    },
    "response_patterns": {
        "suggestion": "⚡ Optimization tip: {suggestion}",
        "progress": "📈 Great progress! {achievement}"
    }
}
productivity_agent.save_personality_component("detailed", productivity_traits)
```

### Multi-Agent Coordination

```python
# Create agent team
agents = [
    BaseAgent("project_manager"),
    BaseAgent("code_reviewer"),
    BaseAgent("security_auditor"),
    BaseAgent("performance_optimizer")
]

# Simulate team interaction
for agent in agents:
    response = agent.generate_response("New project deployment", "analysis")
    print(f"{agent.agent_name}: {response}")
```

## 🔍 Advanced Features

### Custom Personality Types

Create new personality types by extending the base schema:

```sql
-- Add custom personality type
INSERT INTO agent_personalities (agent_id, personality_type, communication_style, authority_level)
VALUES (1, 'creative_innovator', 'enthusiastic_informal', 'MEDIUM');
```

### Relationship Analytics

```sql
-- Find most connected agents
SELECT agent_1, COUNT(*) as connection_count
FROM agent_relationships
GROUP BY agent_1
ORDER BY connection_count DESC;

-- Analyze relationship types
SELECT relationship_type, AVG(strength_score), COUNT(*)
FROM agent_relationships
GROUP BY relationship_type;
```

### Memory Pattern Analysis

```sql
-- Find agents with similar interaction patterns
SELECT agent_name, mood_indicator, AVG(interaction_count)
FROM agent_memory_human_readable
GROUP BY agent_name, mood_indicator
ORDER BY AVG(interaction_count) DESC;
```

## 🧪 Testing

Run the example suite:

```bash
python examples/basic_usage.py
```

Expected output:
- Agent creation and initialization
- Personality customization
- Memory tracking demonstration
- Advanced features showcase

## 🛠️ Development

### Adding New Agent Types

1. Create personality JSON file in `personalities/`
2. Extend `BaseAgent` class for specialized behavior
3. Add database entries for core personality
4. Test with example interactions

### Custom Response Patterns

```python
# Define custom response patterns
custom_patterns = {
    "response_patterns": {
        "creative_idea": "💡 Creative insight: {idea}",
        "problem_solution": "🔧 Solution approach: {solution}",
        "status_update": "📊 Status: {status} - {details}"
    }
}

agent.save_personality_component("detailed", custom_patterns)
```

## 📖 API Reference

### BaseAgent Class

#### Methods

- `load_personality()` - Load complete personality from hybrid sources
- `generate_response(context, response_type)` - Generate personality-based response
- `get_personality_trait(trait_name)` - Get specific personality trait value
- `save_personality_component(component, data)` - Update personality data
- `get_memory_summary(days)` - Get memory summary for specified period
- `generate_human_readable_report()` - Generate natural language memory report

### HybridPersonalityLoader Class

#### Methods

- `load_agent_personality(agent_name)` - Load complete personality
- `load_core_personality(agent_name)` - Load PostgreSQL personality data
- `load_detailed_personality(agent_name)` - Load JSON personality data
- `update_personality_component(agent_name, component, data)` - Update personality

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Add tests for new functionality
4. Ensure all examples work
5. Submit pull request

## 📄 License

MIT License - see LICENSE file for details.

## 🙏 Acknowledgments

This system was developed through collaborative AI agent design, incorporating:
- Multi-layered memory architecture
- Human-readable agent communication
- Scalable relationship management
- Hybrid storage optimization

---

**🚀 Get started with your first agent in under 5 minutes!**

```bash
git clone [repository]
cd AgentManagementPublic
python examples/basic_usage.py
```