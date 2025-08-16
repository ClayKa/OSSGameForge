-- PostgreSQL initialization script for OSSGameForge

-- Create database if not exists (this is usually handled by docker-compose environment variables)
-- CREATE DATABASE IF NOT EXISTS ossgameforge;

-- Connect to the database
\c ossgameforge;

-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create initial schema
CREATE SCHEMA IF NOT EXISTS public;

-- Grant permissions
GRANT ALL ON SCHEMA public TO public;

-- Log successful initialization
DO $$
BEGIN
  RAISE NOTICE 'OSSGameForge database initialized successfully';
END $$;