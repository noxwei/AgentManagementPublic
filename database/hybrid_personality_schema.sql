-- 🧠 Hybrid Personality Storage Schema
-- PostgreSQL extensions for agent personality system
-- Open source release version

-- =====================================================
-- CORE AGENT TABLE
-- =====================================================

CREATE TABLE IF NOT EXISTS agents (
    agent_id SERIAL PRIMARY KEY,
    agent_name VARCHAR(100) UNIQUE NOT NULL,
    category VARCHAR(50) NOT NULL,
    capabilities TEXT[],
    status VARCHAR(20) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- =====================================================
-- CORE PERSONALITY METADATA
-- =====================================================

CREATE TABLE IF NOT EXISTS agent_personalities (
    agent_id INTEGER PRIMARY KEY REFERENCES agents(agent_id) ON DELETE CASCADE,
    personality_type VARCHAR(50) NOT NULL,
    communication_style VARCHAR(50) NOT NULL,
    authority_level VARCHAR(20) NOT NULL,
    cultural_background VARCHAR(100),
    expertise_domains TEXT[],
    management_philosophy TEXT,
    activity_level FLOAT DEFAULT 0.5 CHECK (activity_level >= 0.0 AND activity_level <= 1.0),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- =====================================================
-- AGENT RELATIONSHIPS
-- =====================================================

CREATE TABLE IF NOT EXISTS agent_relationships (
    relationship_id SERIAL PRIMARY KEY,
    agent_1_id INTEGER REFERENCES agents(agent_id) ON DELETE CASCADE,
    agent_2_id INTEGER REFERENCES agents(agent_id) ON DELETE CASCADE,
    relationship_type VARCHAR(50) NOT NULL, -- 'alliance', 'tension', 'neutral', 'mentorship'
    strength_score FLOAT DEFAULT 0.5 CHECK (strength_score >= -1.0 AND strength_score <= 1.0),
    relationship_description TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    last_interaction TIMESTAMP DEFAULT NOW(),
    
    -- Ensure no self-relationships and unique pairs
    CONSTRAINT no_self_relationship CHECK (agent_1_id != agent_2_id),
    CONSTRAINT unique_relationship UNIQUE (agent_1_id, agent_2_id)
);

-- =====================================================
-- MESSAGE TEMPLATES
-- =====================================================

CREATE TABLE IF NOT EXISTS message_templates (
    template_id SERIAL PRIMARY KEY,
    personality_type VARCHAR(50) NOT NULL,
    template_text TEXT NOT NULL,
    template_category VARCHAR(50), -- 'greeting', 'analysis', 'report', 'emergency'
    usage_frequency INTEGER DEFAULT 0,
    success_rate FLOAT DEFAULT 0.0 CHECK (success_rate >= 0.0 AND success_rate <= 1.0),
    last_used TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW()
);

-- =====================================================
-- MEMORY THREAD SUMMARIES
-- =====================================================

CREATE TABLE IF NOT EXISTS agent_memory_summaries (
    memory_id SERIAL PRIMARY KEY,
    agent_id INTEGER REFERENCES agents(agent_id) ON DELETE CASCADE,
    event_date DATE NOT NULL,
    key_events TEXT[],
    interaction_count INTEGER DEFAULT 0,
    mood_indicator VARCHAR(20) DEFAULT 'neutral', -- 'vigilant', 'satisfied', 'concerned', 'neutral'
    primary_context VARCHAR(100),
    learning_insights TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    
    -- One summary per agent per day
    CONSTRAINT unique_daily_summary UNIQUE (agent_id, event_date)
);

-- =====================================================
-- PERSONALITY EVOLUTION TRACKING
-- =====================================================

CREATE TABLE IF NOT EXISTS personality_evolution (
    evolution_id SERIAL PRIMARY KEY,
    agent_id INTEGER REFERENCES agents(agent_id) ON DELETE CASCADE,
    change_type VARCHAR(50) NOT NULL, -- 'template_update', 'relationship_change', 'trait_modification'
    old_value JSONB,
    new_value JSONB,
    change_reason TEXT,
    confidence_score FLOAT DEFAULT 0.5,
    created_at TIMESTAMP DEFAULT NOW()
);

-- =====================================================
-- HUMAN-READABLE VIEWS
-- =====================================================

-- Agent personality overview
CREATE OR REPLACE VIEW agent_personality_overview AS
SELECT 
    a.agent_name,
    a.category,
    ap.personality_type,
    ap.communication_style,
    ap.authority_level,
    ap.cultural_background,
    array_to_string(ap.expertise_domains, ', ') as expertise_summary,
    ap.management_philosophy,
    ap.activity_level,
    ap.updated_at as last_personality_update
FROM agents a
JOIN agent_personalities ap ON a.agent_id = ap.agent_id
ORDER BY a.agent_name;

-- Agent relationship network
CREATE OR REPLACE VIEW agent_relationship_network AS
SELECT 
    a1.agent_name as agent_1,
    a2.agent_name as agent_2,
    ar.relationship_type,
    ar.strength_score,
    ar.relationship_description,
    ar.last_interaction,
    CASE 
        WHEN ar.strength_score > 0.7 THEN '🤝 Strong'
        WHEN ar.strength_score > 0.3 THEN '👥 Moderate'
        WHEN ar.strength_score > -0.3 THEN '😐 Neutral'
        ELSE '⚠️ Tension'
    END as relationship_strength
FROM agent_relationships ar
JOIN agents a1 ON ar.agent_1_id = a1.agent_id
JOIN agents a2 ON ar.agent_2_id = a2.agent_id
ORDER BY ar.strength_score DESC;

-- Human-readable memory summaries
CREATE OR REPLACE VIEW agent_memory_human_readable AS
SELECT 
    a.agent_name,
    ap.personality_type,
    ams.event_date,
    ams.interaction_count,
    ams.mood_indicator,
    CASE 
        WHEN ams.mood_indicator = 'vigilant' THEN '🔍 Alert and monitoring'
        WHEN ams.mood_indicator = 'satisfied' THEN '✅ Content with progress'
        WHEN ams.mood_indicator = 'concerned' THEN '⚠️ Needs attention'
        WHEN ams.mood_indicator = 'focused' THEN '🎯 Highly focused'
        ELSE '📊 Normal operations'
    END as mood_description,
    array_to_string(ams.key_events, '; ') as daily_summary,
    ams.primary_context,
    ams.learning_insights
FROM agents a
JOIN agent_personalities ap ON a.agent_id = ap.agent_id
JOIN agent_memory_summaries ams ON a.agent_id = ams.agent_id
ORDER BY ams.event_date DESC, a.agent_name;

-- Template effectiveness analysis
CREATE OR REPLACE VIEW template_effectiveness AS
SELECT 
    personality_type,
    template_category,
    COUNT(*) as total_templates,
    ROUND(AVG(success_rate)::numeric, 3) as avg_success_rate,
    ROUND(AVG(usage_frequency)::numeric, 1) as avg_usage_frequency,
    MAX(last_used) as most_recent_use
FROM message_templates
GROUP BY personality_type, template_category
ORDER BY avg_success_rate DESC;

-- =====================================================
-- PERFORMANCE INDEXES
-- =====================================================

-- Agent lookups
CREATE INDEX IF NOT EXISTS idx_agents_name ON agents(agent_name);
CREATE INDEX IF NOT EXISTS idx_agents_category ON agents(category);

-- Personality lookups
CREATE INDEX IF NOT EXISTS idx_agent_personalities_type 
ON agent_personalities(personality_type);

CREATE INDEX IF NOT EXISTS idx_agent_personalities_style 
ON agent_personalities(communication_style);

-- Relationship queries
CREATE INDEX IF NOT EXISTS idx_agent_relationships_agent1 
ON agent_relationships(agent_1_id);

CREATE INDEX IF NOT EXISTS idx_agent_relationships_agent2 
ON agent_relationships(agent_2_id);

CREATE INDEX IF NOT EXISTS idx_agent_relationships_type 
ON agent_relationships(relationship_type);

-- Memory summaries
CREATE INDEX IF NOT EXISTS idx_memory_summaries_date 
ON agent_memory_summaries(event_date);

CREATE INDEX IF NOT EXISTS idx_memory_summaries_agent_date 
ON agent_memory_summaries(agent_id, event_date);

-- Template performance
CREATE INDEX IF NOT EXISTS idx_templates_personality_category 
ON message_templates(personality_type, template_category);

CREATE INDEX IF NOT EXISTS idx_templates_success_rate 
ON message_templates(success_rate DESC);

-- =====================================================
-- SECURITY & TRIGGERS
-- =====================================================

-- Update timestamp trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_agents_updated_at
    BEFORE UPDATE ON agents
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_agent_personalities_updated_at
    BEFORE UPDATE ON agent_personalities
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- =====================================================
-- SAMPLE DATA FOR TESTING
-- =====================================================

-- Sample agents
INSERT INTO agents (agent_name, category, capabilities) VALUES
('security_agent', 'security', ARRAY['threat_detection', 'vulnerability_analysis']),
('productivity_agent', 'optimization', ARRAY['workflow_analysis', 'efficiency_optimization']),
('qa_agent', 'quality', ARRAY['code_review', 'testing', 'documentation'])
ON CONFLICT (agent_name) DO NOTHING;

-- Sample personalities
INSERT INTO agent_personalities (agent_id, personality_type, communication_style, authority_level, cultural_background, expertise_domains, management_philosophy, activity_level)
SELECT 
    agent_id,
    CASE 
        WHEN agent_name = 'security_agent' THEN 'security_focused'
        WHEN agent_name = 'productivity_agent' THEN 'efficiency_driven'
        WHEN agent_name = 'qa_agent' THEN 'quality_perfectionist'
    END,
    CASE 
        WHEN agent_name = 'security_agent' THEN 'formal_alert'
        WHEN agent_name = 'productivity_agent' THEN 'encouraging_coach'
        WHEN agent_name = 'qa_agent' THEN 'detailed_helpful'
    END,
    'HIGH',
    CASE 
        WHEN agent_name = 'security_agent' THEN 'Security-first mindset'
        WHEN agent_name = 'productivity_agent' THEN 'Optimization culture'
        WHEN agent_name = 'qa_agent' THEN 'Quality excellence'
    END,
    capabilities,
    CASE 
        WHEN agent_name = 'security_agent' THEN 'Zero tolerance for security vulnerabilities'
        WHEN agent_name = 'productivity_agent' THEN 'Continuous improvement and optimization'
        WHEN agent_name = 'qa_agent' THEN 'Quality through thorough testing and review'
    END,
    0.7
FROM agents 
WHERE agent_name IN ('security_agent', 'productivity_agent', 'qa_agent')
ON CONFLICT (agent_id) DO NOTHING;

-- =====================================================
-- SCHEMA VALIDATION
-- =====================================================

DO $$ 
BEGIN
    RAISE NOTICE '✅ Agent Management Schema Deployment Complete';
    RAISE NOTICE '📊 Tables Created: agents, agent_personalities, agent_relationships, message_templates, agent_memory_summaries, personality_evolution';
    RAISE NOTICE '🔍 Views Created: agent_personality_overview, agent_relationship_network, agent_memory_human_readable, template_effectiveness';
    RAISE NOTICE '⚡ Indexes Created: Performance optimized for personality and relationship queries';
    RAISE NOTICE '🔒 Security: Triggers and constraints implemented';
    RAISE NOTICE '📝 Sample Data: Basic agents and personalities for testing';
END $$;