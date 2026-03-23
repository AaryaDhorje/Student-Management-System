import asyncio
import asyncpg
from datetime import datetime

# Database connection configuration
DB_HOST = "localhost"
DB_PORT = 5432
DB_NAME = "student_management_system"
DB_USER = "postgres"
DB_PASSWORD = "Thor333#"

async def add_soft_delete_columns_to_enrollments():
    """Add soft delete columns to enrollments table"""
    
    # Connect to the database
    conn = await asyncpg.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    
    try:
        print("Adding soft delete columns to enrollments table...")
        
        # Check if columns already exist
        check_deleted_at = """
        SELECT column_name 
        FROM information_schema.columns 
        WHERE table_name = 'enrollments' AND column_name = 'deleted_at'
        """
        
        check_deleted_by = """
        SELECT column_name 
        FROM information_schema.columns 
        WHERE table_name = 'enrollments' AND column_name = 'deleted_by'
        """
        
        deleted_at_exists = await conn.fetchval(check_deleted_at)
        deleted_by_exists = await conn.fetchval(check_deleted_by)
        
        if not deleted_at_exists:
            # Add deleted_at column
            await conn.execute("""
                ALTER TABLE enrollments 
                ADD COLUMN deleted_at TIMESTAMP NULL
            """)
            print("✓ Added deleted_at column")
        else:
            print("✓ deleted_at column already exists")
        
        if not deleted_by_exists:
            # Add deleted_by column
            await conn.execute("""
                ALTER TABLE enrollments 
                ADD COLUMN deleted_by VARCHAR(255) NULL
            """)
            print("✓ Added deleted_by column")
        else:
            print("✓ deleted_by column already exists")
        
        # Create index for deleted_at if it doesn't exist
        await conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_enrollments_deleted_at 
            ON enrollments(deleted_at)
        """)
        print("✓ Created/verified index on deleted_at")
        
        print("\n✅ Soft delete columns added to enrollments table successfully!")
        
    except Exception as e:
        print(f"❌ Error adding soft delete columns: {e}")
        raise
    finally:
        await conn.close()

if __name__ == "__main__":
    asyncio.run(add_soft_delete_columns_to_enrollments())
