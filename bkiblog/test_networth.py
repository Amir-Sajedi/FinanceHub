#!/usr/bin/env python3
"""
Simple test script to verify the net worth feature implementation
"""
import os
import sys

# Add the project directory to Python path
sys.path.insert(0, '/mnt/e/WorkSpace/FinanceHub/bkiblog')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bkiblog.settings')

def check_files():
    """Check if all required files exist"""
    files = [
        '/mnt/e/WorkSpace/FinanceHub/bkiblog/conversionapp/models.py',
        '/mnt/e/WorkSpace/FinanceHub/bkiblog/conversionapp/views.py',
        '/mnt/e/WorkSpace/FinanceHub/bkiblog/conversionapp/urls.py',
        '/mnt/e/WorkSpace/FinanceHub/bkiblog/conversionapp/admin.py',
        '/mnt/e/WorkSpace/FinanceHub/bkiblog/conversionapp/migrations/0001_initial.py',
        '/mnt/e/WorkSpace/FinanceHub/bkiblog/conversionapp/templates/conversionapp/networth.html',
    ]
    
    print("Checking files...")
    for file in files:
        exists = os.path.exists(file)
        status = "✓" if exists else "✗"
        print(f"{status} {file}")
    print()

def check_models():
    """Check if models are properly defined"""
    print("Checking models...")
    try:
        from conversionapp.models import UserHolding, NetWorthHistory
        print("✓ UserHolding model imported successfully")
        print("✓ NetWorthHistory model imported successfully")
        print(f"  - UserHolding fields: {[f.name for f in UserHolding._meta.get_fields()]}")
        print(f"  - NetWorthHistory fields: {[f.name for f in NetWorthHistory._meta.get_fields()]}")
    except Exception as e:
        print(f"✗ Error importing models: {e}")
    print()

def check_views():
    """Check if views are properly defined"""
    print("Checking views...")
    try:
        from conversionapp.views import NetWorthView
        print("✓ NetWorthView imported successfully")
        print(f"  - Template: {NetWorthView.template_name}")
    except Exception as e:
        print(f"✗ Error importing views: {e}")
    print()

def check_urls():
    """Check if URL patterns are configured"""
    print("Checking URLs...")
    try:
        from conversionapp.urls import urlpatterns
        print("✓ URL patterns imported successfully")
        for pattern in urlpatterns:
            print(f"  - {pattern.pattern} -> {pattern.name}")
    except Exception as e:
        print(f"✗ Error importing URLs: {e}")
    print()

if __name__ == '__main__':
    print("=" * 50)
    print("Net Worth Feature - Implementation Verification")
    print("=" * 50)
    print()
    
    check_files()
    
    # Only check Django components if Django is installed
    try:
        import django
        django.setup()
        check_models()
        check_views()
        check_urls()
        print("=" * 50)
        print("Summary: All checks completed!")
        print("=" * 50)
    except ImportError:
        print("Django not available in current environment.")
        print("Run this script in your Django virtual environment to check models/views/urls.")
