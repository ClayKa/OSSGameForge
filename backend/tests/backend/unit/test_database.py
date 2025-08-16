"""
Unit tests for database module
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from sqlalchemy.orm import Session
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', 'backend'))

from backend.app.database import get_db, init_db, check_db_connection, SessionLocal, Base, engine


class TestDatabase:
    """Test database functionality"""
    
    def test_get_db_generator(self):
        """Test get_db yields a session and closes it"""
        with patch('backend.app.database.SessionLocal') as mock_session_local:
            mock_session = Mock(spec=Session)
            mock_session_local.return_value = mock_session
            
            # Get the generator
            db_gen = get_db()
            
            # Get the session
            session = next(db_gen)
            
            # Verify we got the mock session
            assert session == mock_session
            
            # Clean up the generator
            try:
                next(db_gen)
            except StopIteration:
                pass
            
            # Verify close was called
            mock_session.close.assert_called_once()
    
    def test_get_db_cleanup_on_exception(self):
        """Test get_db closes session even on exception"""
        with patch('backend.app.database.SessionLocal') as mock_session_local:
            mock_session = Mock(spec=Session)
            mock_session_local.return_value = mock_session
            
            db_gen = get_db()
            session = next(db_gen)
            
            # Simulate an exception during request
            with pytest.raises(Exception):
                db_gen.throw(Exception("Test exception"))
            
            # Verify close was still called
            mock_session.close.assert_called_once()
    
    @patch('backend.app.database.logger')
    @patch('backend.app.database.Base.metadata.create_all')
    def test_init_db_success(self, mock_create_all, mock_logger):
        """Test successful database initialization"""
        init_db()
        
        # Verify create_all was called with the engine
        mock_create_all.assert_called_once_with(bind=engine)
        
        # Verify success was logged
        mock_logger.info.assert_called_with("Database tables created successfully")
    
    @patch('backend.app.database.logger')
    @patch('backend.app.database.Base.metadata.create_all')
    def test_init_db_failure(self, mock_create_all, mock_logger):
        """Test database initialization failure"""
        mock_create_all.side_effect = Exception("Connection failed")
        
        with pytest.raises(Exception) as exc_info:
            init_db()
        
        assert str(exc_info.value) == "Connection failed"
        mock_logger.error.assert_called()
    
    @patch('backend.app.database.logger')
    @patch('backend.app.database.SessionLocal')
    def test_check_db_connection_success(self, mock_session_local, mock_logger):
        """Test successful database connection check"""
        mock_session = Mock(spec=Session)
        mock_session_local.return_value = mock_session
        
        result = check_db_connection()
        
        assert result == True
        mock_session.execute.assert_called_once_with("SELECT 1")
        mock_session.close.assert_called_once()
        mock_logger.info.assert_called_with("Database connection successful")
    
    @patch('backend.app.database.logger')
    @patch('backend.app.database.SessionLocal')
    def test_check_db_connection_failure(self, mock_session_local, mock_logger):
        """Test failed database connection check"""
        mock_session = Mock(spec=Session)
        mock_session.execute.side_effect = Exception("Connection refused")
        mock_session_local.return_value = mock_session
        
        result = check_db_connection()
        
        assert result == False
        mock_session.execute.assert_called_once_with("SELECT 1")
        mock_logger.error.assert_called()
    
    def test_base_class_exists(self):
        """Test that Base declarative class exists"""
        assert Base is not None
        assert hasattr(Base, 'metadata')
    
    def test_engine_exists(self):
        """Test that engine is created"""
        assert engine is not None
        
    def test_session_local_exists(self):
        """Test that SessionLocal is configured"""
        assert SessionLocal is not None