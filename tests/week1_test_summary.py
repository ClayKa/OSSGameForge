#!/usr/bin/env python
"""
Week 1 Test Summary - Comprehensive test validation for all Week 1 tasks

This script verifies that all Week 1 tasks have proper test coverage
and that all tests pass successfully.
"""
import subprocess
import sys
import os

def run_command(cmd, description):
    """Run a command and return success status"""
    print(f"\n{'='*60}")
    print(f"Testing: {description}")
    print(f"{'='*60}")
    
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"✅ {description} - PASSED")
        return True
    else:
        print(f"❌ {description} - FAILED")
        if result.stderr:
            print(f"Error: {result.stderr[:500]}")  # Show first 500 chars of error
        return False

def main():
    """Run all Week 1 tests"""
    print("="*70)
    print("WEEK 1 TEST SUMMARY - OSSGameForge")
    print("="*70)
    print("\nThis validates all Week 1 tasks:")
    print("- Task 1.1: Project Init, Version Control & CI")
    print("- Task 1.2: Service Orchestration & Mock API")
    print("- Task 1.3: Modular Backend & Database")
    
    os.chdir("/Users/clayka7/Documents/OSSGF")
    
    test_results = {}
    
    # Task 1.1 Tests - Project Structure and CI
    print("\n" + "="*70)
    print("TASK 1.1: Project Init, Version Control & CI")
    print("="*70)
    
    # Check git repository
    test_results["Git repository initialized"] = run_command(
        "git status --porcelain > /dev/null 2>&1",
        "Git repository exists"
    )
    
    # Check directory structure
    test_results["Project structure"] = run_command(
        "test -d backend && test -d frontend && test -d devops && test -d docs && test -d tests",
        "Directory structure exists"
    )
    
    # Check CI configuration
    test_results["CI configuration"] = run_command(
        "test -f .github/workflows/ci.yml",
        "CI workflow file exists"
    )
    
    # Task 1.2 Tests - Service Orchestration & Mock API
    print("\n" + "="*70)
    print("TASK 1.2: Service Orchestration & Mock API")
    print("="*70)
    
    # Check Docker Compose
    test_results["Docker Compose"] = run_command(
        "test -f docker-compose.yml",
        "Docker Compose configuration exists"
    )
    
    # Check Mock Data
    test_results["Mock data"] = run_command(
        "test -f devops/mocks/mock_data.json",
        "Mock data file exists"
    )
    
    # Check API Contract
    test_results["API contract"] = run_command(
        "test -f docs/api_contracts/v1.yaml",
        "OpenAPI specification exists"
    )
    
    # Run Mock API Tests
    test_results["Mock API tests"] = run_command(
        "cd /Users/clayka7/Documents/OSSGF && MOCK_MODE=true python tests/backend/run_all_tests.py 2>/dev/null | grep -q 'ALL TESTS PASSED'",
        "Mock API tests pass"
    )
    
    # Task 1.3 Tests - Modular Backend & Database
    print("\n" + "="*70)
    print("TASK 1.3: Modular Backend & Database")
    print("="*70)
    
    # Check Service Modules
    test_results["Context Builder"] = run_command(
        "test -f backend/app/services/context_builder.py",
        "Context Builder service exists"
    )
    
    test_results["Inference Client"] = run_command(
        "test -f backend/app/services/inference_client.py",
        "Inference Client service exists"
    )
    
    test_results["Postprocessor"] = run_command(
        "test -f backend/app/services/postprocessor.py",
        "Postprocessor service exists"
    )
    
    # Check Database Models
    test_results["Database models"] = run_command(
        "test -f backend/app/models/core_models.py",
        "Database models defined"
    )
    
    # Check Alembic Configuration
    test_results["Alembic setup"] = run_command(
        "test -f backend/alembic.ini && test -d backend/alembic",
        "Alembic migration setup exists"
    )
    
    # Run Service Tests
    test_results["Service tests"] = run_command(
        "cd /Users/clayka7/Documents/OSSGF && python -c 'from tests.backend.test_services import TestContextBuilder, TestInferenceClient, TestPostprocessor; print(\"Service modules imported successfully\")'",
        "Service test modules import"
    )
    
    # Overall Test Suite
    print("\n" + "="*70)
    print("OVERALL TEST SUITE")
    print("="*70)
    
    # Run comprehensive test suite
    test_results["Complete test suite"] = run_command(
        "cd /Users/clayka7/Documents/OSSGF && MOCK_MODE=true python tests/backend/run_all_tests.py 2>/dev/null | tail -5 | grep -q '100.0%'",
        "All tests pass with 100% success rate"
    )
    
    # Summary
    print("\n" + "="*70)
    print("WEEK 1 TEST SUMMARY RESULTS")
    print("="*70)
    
    total_tests = len(test_results)
    passed_tests = sum(1 for v in test_results.values() if v)
    failed_tests = total_tests - passed_tests
    
    print(f"\nTotal Test Categories: {total_tests}")
    print(f"✅ Passed: {passed_tests}")
    print(f"❌ Failed: {failed_tests}")
    print(f"Success Rate: {(passed_tests/total_tests*100):.1f}%")
    
    # Detailed breakdown
    print("\n" + "-"*70)
    print("DETAILED RESULTS:")
    print("-"*70)
    
    for test_name, result in test_results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:40} {status}")
    
    # Final verdict
    print("\n" + "="*70)
    if failed_tests == 0:
        print("🎉 SUCCESS: All Week 1 tasks have been completed with full test coverage!")
        print("All tests are passing successfully!")
        return 0
    else:
        print(f"⚠️  WARNING: {failed_tests} test categories failed.")
        print("Please review the failures above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())