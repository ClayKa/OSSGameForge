#!/bin/bash
# Script to initialize database migrations

echo "========================================="
echo "Initializing Database Migrations"
echo "========================================="

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if running inside container or from host
if [ -f /.dockerenv ]; then
    echo -e "${GREEN}Running inside Docker container${NC}"
    
    # Generate initial migration
    echo -e "${YELLOW}Generating initial migration...${NC}"
    alembic revision --autogenerate -m "Initial migration with Asset, GenerationLog, Project, and Scene tables"
    
    # Apply migrations
    echo -e "${YELLOW}Applying migrations to database...${NC}"
    alembic upgrade head
    
    # Show current revision
    echo -e "${GREEN}Current database revision:${NC}"
    alembic current
    
else
    echo -e "${YELLOW}Running from host - executing inside container${NC}"
    
    # Execute this script inside the backend container
    docker-compose exec backend bash /app/scripts/init_migrations.sh
fi

echo -e "${GREEN}✅ Migration initialization complete!${NC}"