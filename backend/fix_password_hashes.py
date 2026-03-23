import asyncio
import asyncpg
from datetime import datetime
import hashlib
from passlib.context import CryptContext

# Database connection configuration
DB_HOST = "localhost"
DB_PORT = 5432
DB_NAME = "student_management_system"
DB_USER = "postgres"
DB_PASSWORD = "Thor333#"

# Password hashing context (same as auth service)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    """Hash a password using SHA-256 (consistent with existing users)"""
    return hashlib.sha256(password.encode()).hexdigest()

async def check_and_update_passwords():
    """Check current password hashes and update consistently"""
    
    # Connect to the database
    conn = await asyncpg.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    
    try:
        print("Checking current password hashes...")
        
        # Get all users and their password hashes
        users = await conn.fetch("SELECT id, username, password_hash FROM users WHERE deleted_at IS NULL")
        
        for user in users:
            print(f"\n👤 User: {user['username']}")
            print(f"🔐 Current hash: {user['password_hash'][:50]}...")
            
            # Check if it's bcrypt or SHA-256
            if user['password_hash'].startswith('$2b$'):
                print("📋 Hash type: Bcrypt")
            else:
                print("📋 Hash type: SHA-256")
        
        # Update both users to use SHA-256 for consistency
        print("\n🔄 Updating passwords to use SHA-256 for consistency...")
        
        # Update admin password
        admin_password = "Admin@2024Secure!"
        admin_hash = get_password_hash(admin_password)
        await conn.execute("""
            UPDATE users 
            SET password_hash = $1, updated_at = $2
            WHERE username = 'admin'
        """, admin_hash, datetime.utcnow())
        
        # Update staff password  
        staff_password = "staff123"
        staff_hash = get_password_hash(staff_password)
        await conn.execute("""
            UPDATE users 
            SET password_hash = $1, updated_at = $2
            WHERE username = 'staff'
        """, staff_hash, datetime.utcnow())
        
        print("✅ Passwords updated successfully!")
        print("\n🔐 Updated Login Credentials:")
        print("┌─────────────────────────────────────┐")
        print("│ ADMIN USER:                         │")
        print("│ Username: admin                      │")
        print("│ Password: Admin@2024Secure!          │")
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
        print(f"❌ Error updating passwords: {e}")
        raise
    finally:
        await conn.close()

if __name__ == "__main__":
    asyncio.run(check_and_update_passwords())
