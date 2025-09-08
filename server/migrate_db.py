#!/usr/bin/env python3
"""
Database migration script to add new columns for session guidance tracking
"""

import sqlite3
import os
import sys

# Add app directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

def migrate_database():
    """Add new columns to chat_sessions table"""
    db_path = "faq_system.db"
    
    # Check if database exists
    if not os.path.exists(db_path):
        print(f"Database {db_path} does not exist. Creating new database with latest schema.")
        return True
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Check if new columns already exist
        cursor.execute("PRAGMA table_info(chat_sessions)")
        columns = [column[1] for column in cursor.fetchall()]
        
        needs_migration = False
        
        # Add unclear_message_count column if it doesn't exist
        if 'unclear_message_count' not in columns:
            print("Adding unclear_message_count column...")
            cursor.execute("""
                ALTER TABLE chat_sessions 
                ADD COLUMN unclear_message_count INTEGER DEFAULT 0
            """)
            needs_migration = True
        
        # Add guidance_stage column if it doesn't exist
        if 'guidance_stage' not in columns:
            print("Adding guidance_stage column...")
            cursor.execute("""
                ALTER TABLE chat_sessions 
                ADD COLUMN guidance_stage VARCHAR(50) DEFAULT 'normal'
            """)
            needs_migration = True
        
        if needs_migration:
            # Update existing rows with default values
            cursor.execute("""
                UPDATE chat_sessions 
                SET unclear_message_count = 0, guidance_stage = 'normal' 
                WHERE unclear_message_count IS NULL OR guidance_stage IS NULL
            """)
            
            conn.commit()
            print("✅ Database migration completed successfully!")
        else:
            print("✅ Database is already up to date.")
        
        return True
        
    except sqlite3.Error as e:
        print(f"❌ Database migration failed: {e}")
        conn.rollback()
        return False
    
    finally:
        conn.close()

if __name__ == "__main__":
    print("🔄 Starting database migration...")
    success = migrate_database()
    
    if success:
        print("✨ Migration completed. You can now restart the server.")
    else:
        print("💥 Migration failed. Please check the error messages above.")
        sys.exit(1)