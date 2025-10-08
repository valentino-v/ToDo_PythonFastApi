import os
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import ConfigDict

class Settings(BaseSettings):
    """Application settings and configuration"""
    model_config = ConfigDict(
        env_file=".env",
        case_sensitive=False
    )
    
    # App settings
    app_name: str = "ToDo API"
    app_version: str = "1.0.0"
    app_description: str = "A simple ToDo API built with FastAPI"
    
    # Server settings
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = False
    
    # Database settings (for future MySQL integration)
    database_url: Optional[str] = None
    mysql_host: str = "localhost"
    mysql_port: int = 3306
    mysql_user: str = "root"
    mysql_password: str = ""
    mysql_database: str = "todo_db"
    
    # Environment
    environment: str = "development"

    @property
    def mysql_url(self) -> str:
        """Construct MySQL connection URL"""
        return f"mysql+pymysql://{self.mysql_user}:{self.mysql_password}@{self.mysql_host}:{self.mysql_port}/{self.mysql_database}"

# Global settings instance
settings = Settings()