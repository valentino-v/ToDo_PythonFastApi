"""
Tests for configuration module
"""
import pytest
from unittest.mock import patch, MagicMock
from config import Settings

class TestSettings:
    def test_settings_default_values(self):
        """Test default configuration values"""
        settings = Settings()
        assert settings.app_name == "ToDo API"
        assert settings.app_version == "1.0.0"
        assert settings.debug is False
        assert settings.host == "0.0.0.0"
        assert settings.port == 8000

    def test_mysql_url_construction(self):
        """Test MySQL URL construction"""
        settings = Settings(
            mysql_user="test_user",
            mysql_password="test_password", 
            mysql_host="localhost",
            mysql_port=3306,
            mysql_database="test_db"
        )
        
        expected_url = "mysql+pymysql://test_user:test_password@localhost:3306/test_db"
        assert settings.mysql_url == expected_url

    def test_settings_with_env_vars(self):
        """Test settings with environment variables"""
        with patch.dict('os.environ', {
            'APP_NAME': 'Test App',
            'APP_VERSION': '2.0.0',
            'DEBUG': 'true',
            'HOST': '127.0.0.1',
            'PORT': '9000'
        }):
            settings = Settings()
            assert settings.app_name == "Test App"
            assert settings.app_version == "2.0.0"
            assert settings.debug is True
            assert settings.host == "127.0.0.1"
            assert settings.port == 9000

    def test_mysql_settings_with_env_vars(self):
        """Test MySQL settings with environment variables"""
        with patch.dict('os.environ', {
            'MYSQL_HOST': 'db.example.com',
            'MYSQL_PORT': '3307',
            'MYSQL_USER': 'app_user',
            'MYSQL_PASSWORD': 'secret_password',
            'MYSQL_DATABASE': 'production_db'
        }):
            settings = Settings()
            assert settings.mysql_host == "db.example.com"
            assert settings.mysql_port == 3307
            assert settings.mysql_user == "app_user"
            assert settings.mysql_password == "secret_password"
            assert settings.mysql_database == "production_db"
            
            expected_url = "mysql+pymysql://app_user:secret_password@db.example.com:3307/production_db"
            assert settings.mysql_url == expected_url