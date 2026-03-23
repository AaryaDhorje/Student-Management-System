import asyncio
import logging
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

from app.core.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def create_users_table():
    """Create users table with soft delete columns"""
    
    # Create async engine
    engine = create_async_engine(settings.database_url)
    
    try:
        async with engine.begin() as conn:
            # Create users table
            logger.info("Creating users table...")
            
            create_table_sql = """
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                first_name VARCHAR(50) NOT NULL,
                last_name VARCHAR(50) NOT NULL,
                role VARCHAR(20) NOT NULL DEFAULT 'staff',
                is_active BOOLEAN DEFAULT TRUE NOT NULL,
                phone VARCHAR(20),
                department VARCHAR(100),
                created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                deleted_at TIMESTAMP WITH TIME ZONE,
                deleted_by VARCHAR(100)
            );
            """
            
            await conn.execute(text(create_table_sql))
            
            # Create indexes for performance
            logger.info("Creating indexes for users table...")
            
            # Create indexes one by one
            index_statements = [
                "CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);",
                "CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);",
                "CREATE INDEX IF NOT EXISTS idx_users_deleted_at ON users(deleted_at);",
                "CREATE INDEX IF NOT EXISTS idx_users_role ON users(role);",
                "CREATE INDEX IF NOT EXISTS idx_users_is_active ON users(is_active);"
            ]
            
            for index_sql in index_statements:
                await conn.execute(text(index_sql))
            
            logger.info("Users table created successfully!")
            
            # Verify table was created
            verify_sql = """
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns
            WHERE table_name = 'users'
            AND table_schema = 'public'
            ORDER BY ordinal_position;
            """
            
            result = await conn.execute(text(verify_sql))
            columns = result.fetchall()
            
            logger.info("Users table columns:")
            for row in columns:
                logger.info(f"  - {row[0]} ({row[1]}, nullable: {row[2]}")
                
    except Exception as e:
        logger.error(f"Error creating users table: {str(e)}")
        raise
    finally:
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(create_users_table())
