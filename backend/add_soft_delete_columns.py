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

async def add_soft_delete_columns():
    """Add soft delete columns to existing tables"""
    
    engine = create_async_engine(DATABASE_URL, echo=True)
    
    # SQL statements to add soft delete columns
    alter_students_table = """
    ALTER TABLE students 
    ADD COLUMN IF NOT EXISTS deleted_at TIMESTAMP NULL,
    ADD COLUMN IF NOT EXISTS deleted_by VARCHAR(100) NULL;
    """
    
    alter_courses_table = """
    ALTER TABLE courses 
    ADD COLUMN IF NOT EXISTS deleted_at TIMESTAMP NULL,
    ADD COLUMN IF NOT EXISTS deleted_by VARCHAR(100) NULL;
    """
    
    alter_enrollments_table = """
    ALTER TABLE enrollments 
    ADD COLUMN IF NOT EXISTS deleted_at TIMESTAMP NULL,
    ADD COLUMN IF NOT EXISTS deleted_by VARCHAR(100) NULL;
    """
    
    # Create indexes for soft delete performance
    create_soft_delete_indexes = [
        "CREATE INDEX IF NOT EXISTS idx_students_deleted_at ON students(deleted_at);",
        "CREATE INDEX IF NOT EXISTS idx_courses_deleted_at ON courses(deleted_at);",
        "CREATE INDEX IF NOT EXISTS idx_enrollments_deleted_at ON enrollments(deleted_at);"
    ]
    
    try:
        async with engine.begin() as conn:
            print("Adding soft delete columns to students table...")
            await conn.execute(text(alter_students_table))
            
            print("Adding soft delete columns to courses table...")
            await conn.execute(text(alter_courses_table))
            
            print("Adding soft delete columns to enrollments table...")
            await conn.execute(text(alter_enrollments_table))
            
            print("Creating soft delete indexes...")
            for index_sql in create_soft_delete_indexes:
                await conn.execute(text(index_sql))
            
        print("Soft delete columns added successfully!")
        
        # Verify columns exist
        async with engine.begin() as conn:
            # Check students table
            result = await conn.execute(text("""
                SELECT column_name, data_type, is_nullable
                FROM information_schema.columns 
                WHERE table_name = 'students' 
                AND table_schema = 'public'
                ORDER BY ordinal_position;
            """))
            students_columns = result.fetchall()
            
            print("\nStudents table columns:")
            for col in students_columns:
                print(f"  - {col[0]} ({col[1]}, nullable: {col[2]})")
                
    except Exception as e:
        print(f"Error adding soft delete columns: {e}")
        raise
    finally:
        await engine.dispose()

if __name__ == "__main__":
    asyncio.run(add_soft_delete_columns())
