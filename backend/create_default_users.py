import asyncio
import asyncpg
from datetime import datetime

# Database connection configuration
DB_HOST = "localhost"
DB_PORT = 5432
DB_NAME = "student_management_system"
DB_USER = "postgres"
DB_PASSWORD = "Thor333#"

async def create_default_users():
    """Create default admin and staff users"""
    
    # Connect to the database
    conn = await asyncpg.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    
    try:
        print("Creating default users...")
        
        # Hash passwords using SHA-256 (fallback method)
        import hashlib
        admin_password_hash = hashlib.sha256("admin123".encode()).hexdigest()
        staff_password_hash = hashlib.sha256("staff123".encode()).hexdigest()
        
        # Check if users table exists
        check_table = """
        SELECT EXISTS (
            SELECT FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_name = 'users'
        );
        """
        
        table_exists = await conn.fetchval(check_table)
        
        if not table_exists:
            print("❌ Users table does not exist. Please create users table first.")
            return
        
        # Create admin user
        admin_exists = await conn.fetchval(
            "SELECT id FROM users WHERE username = 'admin' OR email = 'admin@sms.com' LIMIT 1"
        )
        
        if not admin_exists:
            await conn.execute("""
                INSERT INTO users (username, email, password_hash, first_name, last_name, role, is_active, phone, department, created_at, updated_at)
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11)
            """, 
            "admin", "admin@sms.com", admin_password_hash, "System", "Administrator", "admin", True, 
            "000-000-0000", "IT Department", datetime.utcnow(), datetime.utcnow()
            )
            print("✓ Created admin user (username: admin, password: admin123)")
        else:
            print("✓ Admin user already exists")
        
        # Create staff user
        staff_exists = await conn.fetchval(
            "SELECT id FROM users WHERE username = 'staff' OR email = 'staff@sms.com' LIMIT 1"
        )
        
        if not staff_exists:
            await conn.execute("""
                INSERT INTO users (username, email, password_hash, first_name, last_name, role, is_active, phone, department, created_at, updated_at)
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11)
            """, 
            "staff", "staff@sms.com", staff_password_hash, "Demo", "Staff", "staff", True, 
            "000-000-0001", "Academic Department", datetime.utcnow(), datetime.utcnow()
            )
            print("✓ Created staff user (username: staff, password: staff123)")
        else:
            print("✓ Staff user already exists")
        
        print("\n✅ Default users created successfully!")
        print("\n🔐 Login Credentials:")
        print("┌─────────────────────────────────────┐")
        print("│ ADMIN USER:                         │")
        print("│ Username: admin                      │")
        print("│ Password: admin123                  │")
        print("│ Email: admin@sms.com                 │")
        print("│ Role: Full Access                    │")
        print("├─────────────────────────────────────┤")
        print("│ STAFF USER:                         │")
        print("│ Username: staff                      │")
        print("│ Password: staff123                  │")
        print("│ Email: staff@sms.com                 │")
        print("│ Role: Limited Access                 │")
        print("└─────────────────────────────────────┘")
        
    except Exception as e:
        print(f"❌ Error creating default users: {e}")
        raise
    finally:
        await conn.close()

if __name__ == "__main__":
    asyncio.run(create_default_users())
