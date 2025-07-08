#!/usr/bin/env python3
"""
🚀 Basic Usage Examples
=======================

This file demonstrates basic usage of the Agent Management System
with hybrid personality storage.

Public release version - sanitized for open source distribution.
"""

import sys
import json
from pathlib import Path

# Add project paths
sys.path.append("../core")
sys.path.append("../agents")

from hybrid_personality_loader import HybridPersonalityLoader
from base_agent import BaseAgent

def example_1_create_simple_agent():
    """Example 1: Create and interact with a simple agent"""
    print("🤖 Example 1: Creating a Simple Agent")
    print("=" * 50)
    
    # Create agent
    agent = BaseAgent("example_agent")
    
    # Test basic interactions
    greeting = agent.generate_response("Hello there!", "greeting")
    analysis = agent.generate_response("System performance analysis", "analysis")
    completion = agent.generate_response("Data processing task", "completion")
    
    print(f"Greeting: {greeting}")
    print(f"Analysis: {analysis}")
    print(f"Completion: {completion}")
    
    # Show personality traits
    print(f"\nPersonality Traits:")
    for trait, value in agent.personality["detailed_traits"].items():
        print(f"  {trait}: {value}")
    
    return agent

def example_2_customize_personality():
    """Example 2: Customize agent personality"""
    print("\n🎨 Example 2: Customizing Agent Personality")
    print("=" * 50)
    
    # Create agent
    agent = BaseAgent("custom_agent")
    
    # Update personality traits
    new_traits = {
        "detailed_traits": {
            "creativity": 0.9,
            "humor": 0.7,
            "precision": 0.8,
            "enthusiasm": 0.9
        },
        "response_patterns": {
            "greeting": "🎉 Hey there! I'm {agent_name}, your creative assistant!",
            "analysis": "🔍 Creative analysis of {context}: {findings} ✨",
            "completion": "🎯 Mission accomplished: {summary} 🚀"
        }
    }
    
    # Save updated traits
    agent.save_personality_component("detailed", new_traits)
    
    # Test customized responses
    greeting = agent.generate_response("Hi!", "greeting")
    analysis = agent.generate_response("Creative project brainstorming", "analysis")
    
    print(f"Custom Greeting: {greeting}")
    print(f"Custom Analysis: {analysis}")
    
    return agent

def example_3_memory_tracking():
    """Example 3: Memory tracking and reporting"""
    print("\n📚 Example 3: Memory Tracking and Reporting")
    print("=" * 50)
    
    # Create agent
    agent = BaseAgent("memory_agent")
    
    # Simulate multiple interactions
    interactions = [
        ("Good morning", "greeting"),
        ("Analyze user feedback", "analysis"),
        ("Process data batch", "completion"),
        ("Review security logs", "analysis"),
        ("Generate report", "completion")
    ]
    
    for context, response_type in interactions:
        response = agent.generate_response(context, response_type)
        print(f"  {response_type}: {response}")
    
    # Generate memory report
    print("\n📋 Memory Report:")
    print(agent.generate_human_readable_report())
    
    return agent

def example_4_personality_loader():
    """Example 4: Direct personality loader usage"""
    print("\n🧠 Example 4: Direct Personality Loader Usage")
    print("=" * 50)
    
    # Initialize loader
    loader = HybridPersonalityLoader(json_dir="../personalities")
    
    # Load existing personality
    personality = loader.load_agent_personality("security_agent")
    
    if personality:
        print("Loaded Security Agent Personality:")
        print(f"  Type: {personality['core_personality'].get('personality_type', 'Unknown')}")
        print(f"  Communication: {personality['core_personality'].get('communication_style', 'Unknown')}")
        print(f"  Risk Tolerance: {personality['detailed_traits'].get('risk_tolerance', 'Unknown')}")
        print(f"  Response Patterns: {len(personality['response_patterns'])} patterns")
    else:
        print("No personality found - creating new one")
        
        # Create sample personality
        sample_personality = {
            "detailed_traits": {
                "analytical_thinking": 0.8,
                "communication_clarity": 0.7,
                "problem_solving": 0.9
            },
            "response_patterns": {
                "greeting": "Hello! I'm ready to analyze and solve problems.",
                "analysis": "Analyzing {context}: {findings}",
                "completion": "Analysis complete: {summary}"
            },
            "learning_history": [],
            "contextual_memories": []
        }
        
        # Save new personality
        success = loader.update_detailed_personality("new_agent", sample_personality)
        print(f"Created new personality: {success}")

def example_5_advanced_features():
    """Example 5: Advanced features demonstration"""
    print("\n🚀 Example 5: Advanced Features")
    print("=" * 50)
    
    # Create specialized agents
    security_agent = BaseAgent("security_demo")
    productivity_agent = BaseAgent("productivity_demo")
    
    # Update security agent with specialized traits
    security_traits = {
        "detailed_traits": {
            "security_focus": 0.95,
            "threat_detection": 0.9,
            "risk_assessment": 0.85,
            "compliance_awareness": 0.8
        },
        "response_patterns": {
            "threat_alert": "🚨 SECURITY THREAT: {threat} - Immediate action required!",
            "all_clear": "✅ Security scan complete - No threats detected",
            "recommendation": "🛡️ Security Recommendation: {advice}"
        }
    }
    
    productivity_traits = {
        "detailed_traits": {
            "efficiency_optimization": 0.9,
            "workflow_analysis": 0.85,
            "time_management": 0.8,
            "motivation": 0.9
        },
        "response_patterns": {
            "optimization": "⚡ Optimization Opportunity: {opportunity}",
            "progress": "📈 Progress Update: {status}",
            "motivation": "💪 Keep going! {encouragement}"
        }
    }
    
    # Apply specialized traits
    security_agent.save_personality_component("detailed", security_traits)
    productivity_agent.save_personality_component("detailed", productivity_traits)
    
    # Demonstrate specialized responses
    print("Security Agent Response:")
    print(f"  {security_agent.get_response_pattern('threat_alert', threat='Unauthorized access attempt')}")
    print(f"  {security_agent.get_response_pattern('all_clear')}")
    
    print("\nProductivity Agent Response:")
    print(f"  {productivity_agent.get_response_pattern('optimization', opportunity='Automate daily reports')}")
    print(f"  {productivity_agent.get_response_pattern('motivation', encouragement='You have completed 80% of your goals!')}")

def main():
    """Run all examples"""
    print("🎯 Agent Management System - Usage Examples")
    print("=" * 60)
    
    # Run examples
    agent1 = example_1_create_simple_agent()
    agent2 = example_2_customize_personality()
    agent3 = example_3_memory_tracking()
    example_4_personality_loader()
    example_5_advanced_features()
    
    print("\n✅ All examples completed successfully!")
    print("\nNext Steps:")
    print("1. 📖 Read the documentation in ../docs/")
    print("2. 🗄️ Set up PostgreSQL database using ../database/hybrid_personality_schema.sql")
    print("3. 🎨 Create custom personality JSON files in ../personalities/")
    print("4. 🤖 Build your own specialized agents using BaseAgent class")

if __name__ == "__main__":
    main()