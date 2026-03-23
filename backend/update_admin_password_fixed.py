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
    """Hash a password using the same method as auth service"""
    try:
        return pwd_context.hash(password)
    except:
        # Fallback to SHA-256 if bcrypt fails
        return hashlib.sha256(password.encode()).hexdigest()

async def update_admin_password():
    """Update admin password using proper hashing"""
    
    # Connect to the database
    conn = await asyncpg.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    
    try:
        print("Updating admin password with proper hashing...")
        
        # New strong password
        new_password = "Admin@2024Secure!"
        password_hash = get_password_hash(new_password)
        
        print(f"🔐 Generated hash: {password_hash[:50]}...")
        
        # Update admin password
        await conn.execute("""
            UPDATE users 
            SET password_hash = $1, updated_at = $2
            WHERE username = 'admin'
        """, password_hash, datetime.utcnow())
        
        print("✅ Admin password updated successfully!")
        print("\n🔐 New Login Credentials:")
        print("┌─────────────────────────────────────┐")
        print("│ ADMIN USER:                         │")
        print("│ Username: admin                      │")
        print("│ Password: Admin@2024Secure!          │")
        print("│ Email: admin@sms.com                 │")
        print("│ Role: Full Access                    │")
        print("└─────────────────────────────────────┘")
        print("\n📝 Staff credentials remain the same:")
        print("┌─────────────────────────────────────┐")
        print("│ STAFF USER:                         │")
        print("│ Username: staff                      │")
        print("│ Password: staff123                  │")
        print("│ Email: staff@sms.com                 │")
        print("│ Role: Limited Access                 │")
        print("└─────────────────────────────────────┘")
        
    except Exception as e:
        print(f"❌ Error updating password: {e}")
        raise
    finally:
        await conn.close()

if __name__ == "__main__":
    asyncio.run(update_admin_password())
