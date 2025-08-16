#!/usr/bin/env python
"""
Test script to verify database connectivity and table creation

Run this inside the Docker container to verify Task 1.3 completion.
"""
import sys

sys.path.insert(0, '/app')

import logging

from app.database import SessionLocal, check_db_connection, engine
from app.models import Asset, GenerationLog, Project, Scene
from sqlalchemy import inspect

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def test_database_connection():
    """Test basic database connectivity"""
    print("\n" + "="*60)
    print("Testing Database Connection")
    print("="*60)

    if check_db_connection():
        print("✅ Database connection successful")
        return True
    else:
        print("❌ Database connection failed")
        return False


def test_tables_exist():
    """Verify that all required tables exist"""
    print("\n" + "="*60)
    print("Verifying Database Tables")
    print("="*60)

    inspector = inspect(engine)
    existing_tables = inspector.get_table_names()

    required_tables = ['assets', 'generation_logs', 'projects', 'scenes']

    all_exist = True
    for table in required_tables:
        if table in existing_tables:
            print(f"✅ Table '{table}' exists")
        else:
            print(f"❌ Table '{table}' is missing")
            all_exist = False

    # Show any additional tables
    extra_tables = set(existing_tables) - set(required_tables)
    if extra_tables:
        print(f"\nAdditional tables found: {extra_tables}")

    return all_exist


def test_table_columns():
    """Verify that tables have the correct columns"""
    print("\n" + "="*60)
    print("Verifying Table Schemas")
    print("="*60)

    inspector = inspect(engine)

    # Define expected columns for each table
    expected_columns = {
        'assets': ['id', 'project_id', 'path', 'type', 'status', 'metadata',
                   'consent_hash', 'exif_stripped', 'created_at', 'updated_at'],
        'generation_logs': ['id', 'user_id', 'input_hash', 'prompt_hash',
                           'model_version', 'lora_adapter', 'status',
                           'latency_ms', 'error', 'created_at'],
        'projects': ['id', 'name', 'description', 'owner', 'status',
                    'settings', 'created_at', 'updated_at'],
        'scenes': ['id', 'project_id', 'name', 'style', 'scene_data',
                  'thumbnail_path', 'generation_log_id', 'created_at', 'updated_at']
    }

    all_correct = True
    for table_name, expected_cols in expected_columns.items():
        print(f"\n{table_name} table:")

        try:
            columns = [col['name'] for col in inspector.get_columns(table_name)]

            # Check for expected columns
            for col in expected_cols:
                if col in columns:
                    print(f"  ✅ Column '{col}' exists")
                else:
                    print(f"  ❌ Column '{col}' is missing")
                    all_correct = False

            # Show any extra columns
            extra_cols = set(columns) - set(expected_cols)
            if extra_cols:
                print(f"  ℹ️  Additional columns: {extra_cols}")

        except Exception as e:
            print(f"  ❌ Error inspecting table: {e}")
            all_correct = False

    return all_correct


def test_crud_operations():
    """Test basic CRUD operations"""
    print("\n" + "="*60)
    print("Testing CRUD Operations")
    print("="*60)

    db = SessionLocal()

    try:
        # Test Project creation
        test_project = Project(
            name="Test Project",
            description="Created by test script",
            owner="test_user"
        )
        db.add(test_project)
        db.commit()
        print(f"✅ Created project: {test_project.id}")

        # Test Asset creation
        test_asset = Asset(
            project_id=str(test_project.id),
            path="/test/path/image.png",
            type="image",
            consent_hash="test_hash_123",
            exif_stripped=True
        )
        db.add(test_asset)
        db.commit()
        print(f"✅ Created asset: {test_asset.id}")

        # Test GenerationLog creation
        test_log = GenerationLog(
            user_id="test_user",
            input_hash="input_123",
            prompt_hash="prompt_456",
            model_version="test_v1",
            status="success",
            latency_ms=1000
        )
        db.add(test_log)
        db.commit()
        print(f"✅ Created generation log: {test_log.id}")

        # Test Scene creation
        test_scene = Scene(
            project_id=str(test_project.id),
            name="Test Scene",
            style="platformer",
            scene_data={"entities": [], "metadata": {}}
        )
        db.add(test_scene)
        db.commit()
        print(f"✅ Created scene: {test_scene.id}")

        # Test reading
        project_count = db.query(Project).count()
        asset_count = db.query(Asset).count()
        log_count = db.query(GenerationLog).count()
        scene_count = db.query(Scene).count()

        print("\n📊 Database Statistics:")
        print(f"  Projects: {project_count}")
        print(f"  Assets: {asset_count}")
        print(f"  Generation Logs: {log_count}")
        print(f"  Scenes: {scene_count}")

        # Clean up test data
        db.query(Scene).filter_by(id=test_scene.id).delete()
        db.query(Asset).filter_by(id=test_asset.id).delete()
        db.query(GenerationLog).filter_by(id=test_log.id).delete()
        db.query(Project).filter_by(id=test_project.id).delete()
        db.commit()
        print("\n🧹 Test data cleaned up")

        return True

    except Exception as e:
        print(f"❌ CRUD operation failed: {e}")
        db.rollback()
        return False
    finally:
        db.close()


def main():
    """Run all database tests"""
    print("="*70)
    print("OSSGameForge Database Verification")
    print("Task 1.3 Completion Test")
    print("="*70)

    results = {
        "Connection": test_database_connection(),
        "Tables Exist": test_tables_exist(),
        "Table Schemas": test_table_columns(),
        "CRUD Operations": test_crud_operations()
    }

    # Summary
    print("\n" + "="*70)
    print("Test Summary")
    print("="*70)

    all_passed = True
    for test_name, passed in results.items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{test_name}: {status}")
        if not passed:
            all_passed = False

    if all_passed:
        print("\n🎉 All database tests passed! Task 1.3 is complete!")
        return 0
    else:
        print("\n⚠️  Some tests failed. Please review the errors above.")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
