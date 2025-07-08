# 🚀 Installation Guide

Complete setup guide for the Agent Management System with hybrid personality storage.

## 📋 Prerequisites

### System Requirements
- **Python**: 3.8 or higher
- **PostgreSQL**: 12 or higher
- **Operating System**: macOS, Linux, or Windows
- **Memory**: 512MB RAM minimum
- **Storage**: 100MB for base installation

### Python Dependencies
- `psycopg2-binary` - PostgreSQL adapter
- `pathlib` - Path handling (built-in Python 3.4+)
- `json` - JSON processing (built-in)
- `datetime` - Timestamp handling (built-in)

## 🗄️ Database Setup

### Option 1: Local PostgreSQL Installation

#### macOS (using Homebrew)
```bash
# Install PostgreSQL
brew install postgresql

# Start PostgreSQL service
brew services start postgresql

# Create database
createdb agent_system

# Create user (optional)
psql postgres -c "CREATE USER agent_user WITH PASSWORD 'your_password';"
psql postgres -c "GRANT ALL PRIVILEGES ON DATABASE agent_system TO agent_user;"
```

#### Ubuntu/Debian
```bash
# Update package list
sudo apt update

# Install PostgreSQL
sudo apt install postgresql postgresql-contrib

# Start PostgreSQL service
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Switch to postgres user and create database
sudo -u postgres createdb agent_system
sudo -u postgres createuser agent_user

# Set password for user
sudo -u postgres psql -c "ALTER USER agent_user PASSWORD 'your_password';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE agent_system TO agent_user;"
```

#### Windows
1. Download PostgreSQL installer from [postgresql.org](https://www.postgresql.org/download/windows/)
2. Run installer and follow setup wizard
3. Remember the password for the `postgres` user
4. Open pgAdmin or use command line to create database:
```sql
CREATE DATABASE agent_system;
CREATE USER agent_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE agent_system TO agent_user;
```

### Option 2: Docker PostgreSQL

```bash
# Pull PostgreSQL image
docker pull postgres:13

# Run PostgreSQL container
docker run --name agent-postgres \
  -e POSTGRES_DB=agent_system \
  -e POSTGRES_USER=agent_user \
  -e POSTGRES_PASSWORD=your_password \
  -p 5432:5432 \
  -d postgres:13

# Verify container is running
docker ps
```

### Option 3: Cloud PostgreSQL

#### AWS RDS
1. Go to AWS RDS Console
2. Create new PostgreSQL instance
3. Choose instance class and storage
4. Set master username and password
5. Configure security groups for access
6. Note the endpoint URL

#### Google Cloud SQL
```bash
# Create instance using gcloud CLI
gcloud sql instances create agent-postgres \
  --database-version=POSTGRES_13 \
  --tier=db-f1-micro \
  --region=us-central1

# Create database
gcloud sql databases create agent_system --instance=agent-postgres

# Create user
gcloud sql users create agent_user --instance=agent-postgres --password=your_password
```

## 🏗️ Schema Installation

### Load Database Schema

```bash
# Navigate to project directory
cd AgentManagementPublic

# Load schema (replace with your connection details)
psql -h localhost -d agent_system -U agent_user -f database/hybrid_personality_schema.sql
```

### Verify Schema Installation

```sql
-- Connect to database
psql -h localhost -d agent_system -U agent_user

-- Check tables were created
\dt

-- Expected output:
--  agent_personalities
--  agent_relationships  
--  agent_memory_summaries
--  agents
--  message_templates
--  personality_evolution

-- Check views were created
\dv

-- Expected output:
--  agent_memory_human_readable
--  agent_personality_overview
--  agent_relationship_network
--  template_effectiveness

-- Exit psql
\q
```

## 🐍 Python Environment Setup

### Option 1: Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv agent_env

# Activate virtual environment
# On macOS/Linux:
source agent_env/bin/activate
# On Windows:
agent_env\Scripts\activate

# Install dependencies
pip install psycopg2-binary

# Verify installation
python -c "import psycopg2; print('psycopg2 installed successfully')"
```

### Option 2: System Installation

```bash
# Install psycopg2-binary globally
pip install psycopg2-binary

# For Ubuntu/Debian, you might need:
sudo apt-get install python3-dev libpq-dev
pip install psycopg2-binary
```

### Option 3: Conda Environment

```bash
# Create conda environment
conda create -n agent_env python=3.9

# Activate environment
conda activate agent_env

# Install dependencies
conda install -c conda-forge psycopg2
```

## ⚙️ Configuration

### Database Configuration

#### Option 1: Environment Variables
```bash
# Add to your ~/.bashrc, ~/.zshrc, or .env file
export DB_HOST=localhost
export DB_NAME=agent_system
export DB_USER=agent_user
export DB_PASSWORD=your_password
export DB_PORT=5432
```

#### Option 2: Configuration File
Create `config.json` in the project root:
```json
{
  "host": "localhost",
  "database": "agent_system", 
  "user": "agent_user",
  "password": "your_password",
  "port": 5432
}
```

#### Option 3: Direct Configuration
Modify the configuration in your code:
```python
from core.hybrid_personality_loader import HybridPersonalityLoader

# Custom configuration
config = {
    "host": "your-db-host.com",
    "database": "agent_system",
    "user": "agent_user", 
    "password": "your_password",
    "port": 5432
}

# Initialize with custom config
loader = HybridPersonalityLoader(config_path=None)
loader.db_config = config
```

## ✅ Installation Verification

### Test Database Connection

```python
# test_installation.py
import psycopg2
import os

# Test database connection
try:
    conn = psycopg2.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        database=os.getenv('DB_NAME', 'agent_system'),
        user=os.getenv('DB_USER', 'agent_user'),
        password=os.getenv('DB_PASSWORD', 'your_password'),
        port=os.getenv('DB_PORT', 5432)
    )
    
    with conn.cursor() as cur:
        cur.execute("SELECT version();")
        version = cur.fetchone()
        print(f"✅ Database connection successful!")
        print(f"PostgreSQL version: {version[0]}")
        
        # Test schema
        cur.execute("SELECT COUNT(*) FROM agents;")
        count = cur.fetchone()[0]
        print(f"✅ Schema loaded successfully! Found {count} sample agents.")
        
    conn.close()
    
except Exception as e:
    print(f"❌ Database connection failed: {e}")
```

### Test Agent System

```python
# test_agents.py
from agents.base_agent import BaseAgent

try:
    # Create test agent
    agent = BaseAgent("test_agent")
    
    # Test basic functionality
    greeting = agent.generate_response("Hello", "greeting")
    print(f"✅ Agent creation successful!")
    print(f"Response: {greeting}")
    
    # Test personality loading
    personality_type = agent.personality["core_personality"].get("personality_type")
    print(f"✅ Personality loading successful! Type: {personality_type}")
    
    # Test memory report
    report = agent.generate_human_readable_report()
    print(f"✅ Memory system working!")
    
except Exception as e:
    print(f"❌ Agent system test failed: {e}")
```

### Run Example Suite

```bash
# Run all examples
python examples/basic_usage.py

# Expected output:
# 🤖 Example 1: Creating a Simple Agent
# 🎨 Example 2: Customizing Agent Personality  
# 📚 Example 3: Memory Tracking and Reporting
# 🧠 Example 4: Direct Personality Loader Usage
# 🚀 Example 5: Advanced Features
# ✅ All examples completed successfully!
```

## 🛠️ Troubleshooting

### Common Issues

#### 1. PostgreSQL Connection Error
```
psycopg2.OperationalError: could not connect to server
```

**Solutions:**
- Verify PostgreSQL is running: `brew services list` (macOS) or `sudo systemctl status postgresql` (Linux)
- Check connection details in configuration
- Verify database and user exist
- Check firewall settings

#### 2. Permission Denied Error
```
psycopg2.errors.InsufficientPrivilege: permission denied for table agents
```

**Solutions:**
```sql
-- Grant permissions to user
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO agent_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO agent_user;
```

#### 3. Module Import Error
```
ModuleNotFoundError: No module named 'psycopg2'
```

**Solutions:**
- Ensure virtual environment is activated
- Install psycopg2-binary: `pip install psycopg2-binary`
- On Linux, install dev packages: `sudo apt-get install python3-dev libpq-dev`

#### 4. Schema Already Exists
```
ERROR: relation "agents" already exists
```

**Solutions:**
- Drop existing schema: `DROP SCHEMA public CASCADE; CREATE SCHEMA public;`
- Or use schema with conflict handling already built-in (CREATE IF NOT EXISTS)

#### 5. JSON File Permissions
```
PermissionError: [Errno 13] Permission denied
```

**Solutions:**
```bash
# Fix directory permissions
chmod 755 personalities/
chmod 644 personalities/*.json
```

### Performance Optimization

#### Database Performance
```sql
-- Analyze tables for better query planning
ANALYZE agents;
ANALYZE agent_personalities;
ANALYZE agent_relationships;

-- Check index usage
SELECT schemaname, tablename, indexname, idx_scan 
FROM pg_stat_user_indexes 
ORDER BY idx_scan DESC;
```

#### Memory Optimization
```python
# For large agent populations, consider connection pooling
import psycopg2.pool

# Create connection pool
pool = psycopg2.pool.SimpleConnectionPool(
    1, 20,  # min and max connections
    host="localhost",
    database="agent_system",
    user="agent_user",
    password="your_password"
)
```

## 🔄 Maintenance

### Regular Tasks

#### Database Maintenance
```sql
-- Weekly vacuum and analyze
VACUUM ANALYZE;

-- Check database size
SELECT pg_size_pretty(pg_database_size('agent_system'));

-- Monitor active connections
SELECT count(*) FROM pg_stat_activity WHERE datname = 'agent_system';
```

#### Log Rotation
```bash
# Setup logrotate for agent logs
sudo tee /etc/logrotate.d/agent-management << EOF
/path/to/AgentManagementPublic/logs/*.log {
    daily
    missingok
    rotate 30
    compress
    notifempty
    create 644 root root
}
EOF
```

### Backup Strategy

#### Database Backup
```bash
# Create backup
pg_dump -h localhost -U agent_user agent_system > backup_$(date +%Y%m%d).sql

# Restore from backup
psql -h localhost -U agent_user agent_system < backup_20250108.sql
```

#### Personality Files Backup
```bash
# Backup personality files
tar -czf personalities_backup_$(date +%Y%m%d).tar.gz personalities/

# Restore personality files
tar -xzf personalities_backup_20250108.tar.gz
```

## 🎯 Next Steps

After successful installation:

1. **🔍 Explore Examples**: Run `python examples/basic_usage.py`
2. **📖 Read Documentation**: Check `docs/ARCHITECTURE.md`
3. **🎨 Create Custom Agents**: Extend `BaseAgent` class
4. **🗄️ Design Personalities**: Create JSON personality files
5. **📊 Setup Monitoring**: Implement logging and analytics

Your Agent Management System is now ready for use! 🚀