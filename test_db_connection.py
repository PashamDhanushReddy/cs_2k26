#!/usr/bin/env python
"""Test script to verify Neon database connection"""

import os
import psycopg2
from psycopg2.extras import RealDictCursor

def test_connection():
    """Test the Neon database connection"""
    try:
        # Get the database URL from environment variable
        conn_str = os.environ.get('NEON_DATABASE_URL')
        if not conn_str:
            print("❌ NEON_DATABASE_URL environment variable not set")
            return False
        
        print(f"🔗 Connecting to database...")
        
        # Connect to the database
        conn = psycopg2.connect(conn_str)
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        # Test the connection with a simple query
        cur.execute("SELECT version();")
        version = cur.fetchone()
        print(f"✅ Database connection successful!")
        print(f"📊 Database version: {version['version']}")
        
        # Check if the registrations table exists
        cur.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_name = 'codestorm_registrations';
        """)
        table_exists = cur.fetchone()
        
        if table_exists:
            print("✅ codestorm_registrations table found!")
            
            # Get table structure
            cur.execute("""
                SELECT column_name, data_type, is_nullable, column_default
                FROM information_schema.columns
                WHERE table_name = 'codestorm_registrations'
                ORDER BY ordinal_position;
            """)
            columns = cur.fetchall()
            print(f"📋 Table has {len(columns)} columns")
            
        else:
            print("⚠️  codestorm_registrations table not found")
        
        # Close the connection
        cur.close()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"❌ Database connection failed: {str(e)}")
        return False

if __name__ == "__main__":
    print("🧪 Testing Neon Database Connection")
    print("=" * 40)
    success = test_connection()
    print("=" * 40)
    if success:
        print("🎉 Database connection test completed successfully!")
    else:
        print("💥 Database connection test failed!")