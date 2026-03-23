import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text

# Database configuration
DB_HOST = "localhost"
DB_PORT = 5432
DB_NAME = "student_management_system"
DB_USER = "postgres"
DB_PASSWORD = "Thor333#"

DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

async def create_tables():
    """Drop existing tables and recreate with integer primary keys"""
    
    engine = create_async_engine(DATABASE_URL, echo=True)
    
    # Drop existing tables first
    drop_tables = [
        "DROP TABLE IF EXISTS enrollments CASCADE;",
        "DROP TABLE IF EXISTS courses CASCADE;",
        "DROP TABLE IF EXISTS students CASCADE;"
    ]
    
    # SQL statements to create tables with integer primary keys
    create_students_table = """
    CREATE TABLE students (
        id SERIAL PRIMARY KEY,
        first_name VARCHAR(100) NOT NULL,
        last_name VARCHAR(100) NOT NULL,
        email VARCHAR(255) NOT NULL UNIQUE,
        enrollment_date DATE NOT NULL,
        is_active BOOLEAN DEFAULT TRUE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    
    create_courses_table = """
    CREATE TABLE courses (
        id SERIAL PRIMARY KEY,
        course_name VARCHAR(150) NOT NULL,
        course_code VARCHAR(50) NOT NULL UNIQUE,
        description TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    
    create_enrollments_table = """
    CREATE TABLE enrollments (
        id SERIAL PRIMARY KEY,
        student_id INTEGER NOT NULL REFERENCES students(id),
        course_id INTEGER NOT NULL REFERENCES courses(id),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        CONSTRAINT uq_student_course UNIQUE (student_id, course_id)
    );
    """
    
    # Create indexes
    create_indexes = [
        "CREATE INDEX idx_students_email ON students(email);",
        "CREATE INDEX idx_courses_course_code ON courses(course_code);",
        "CREATE INDEX idx_enrollments_student_id ON enrollments(student_id);",
        "CREATE INDEX idx_enrollments_course_id ON enrollments(course_id);"
    ]
    
    try:
        async with engine.begin() as conn:
            print("Dropping existing tables...")
            for drop_sql in drop_tables:
                await conn.execute(text(drop_sql))
            
            print("Creating students table...")
            await conn.execute(text(create_students_table))
            
            print("Creating courses table...")
            await conn.execute(text(create_courses_table))
            
            print("Creating enrollments table...")
            await conn.execute(text(create_enrollments_table))
            
            print("Creating indexes...")
            for index_sql in create_indexes:
                await conn.execute(text(index_sql))
            
        print("All tables recreated successfully with integer primary keys!")
        
        # Verify tables exist
        async with engine.begin() as conn:
            result = await conn.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_type = 'BASE TABLE'
                ORDER BY table_name;
            """))
            tables = result.fetchall()
            
            print("\nTables in database:")
            for table in tables:
                print(f"  - {table[0]}")
                
    except Exception as e:
        print(f"Error creating tables: {e}")
        raise
    finally:
        await engine.dispose()

if __name__ == "__main__":
    asyncio.run(create_tables())
