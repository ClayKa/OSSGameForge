#!/usr/bin/env python
"""
Standalone test runner for project structure tests
"""
import os
import sys
import unittest

# Add tests directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'tests'))


def run_structure_tests():
    """Run tests to verify project structure"""
    
    test_results = []
    
    print("=" * 60)
    print("Running OSSGameForge Project Structure Tests")
    print("=" * 60)
    
    # Test categories
    tests = {
        "Project Structure": [
            ("Backend directory", os.path.exists("backend")),
            ("Frontend directory", os.path.exists("frontend")),
            ("Docker Compose file", os.path.exists("docker-compose.yml")),
            ("README.md", os.path.exists("README.md")),
            ("LICENSE", os.path.exists("LICENSE")),
            ("Makefile", os.path.exists("Makefile")),
        ],
        "Backend Structure": [
            ("app/main.py", os.path.exists("backend/app/main.py")),
            ("app/config.py", os.path.exists("backend/app/config.py")),
            ("app/database.py", os.path.exists("backend/app/database.py")),
            ("requirements.txt", os.path.exists("backend/requirements.txt")),
            ("requirements-dev.txt", os.path.exists("backend/requirements-dev.txt")),
            ("Dockerfile", os.path.exists("backend/Dockerfile")),
        ],
        "CI/CD Configuration": [
            (".github/workflows/ci.yml", os.path.exists(".github/workflows/ci.yml")),
            (".pre-commit-config.yaml", os.path.exists(".pre-commit-config.yaml")),
            ("pyproject.toml", os.path.exists("pyproject.toml")),
        ],
        "Documentation": [
            ("CONTRIBUTING.md", os.path.exists("CONTRIBUTING.md")),
            ("CLAUDE.md", os.path.exists("CLAUDE.md")),
            ("ROADMAP.md", os.path.exists("ROADMAP.md")),
            ("PR template", os.path.exists(".github/pull_request_template.md")),
            ("Bug report template", os.path.exists(".github/ISSUE_TEMPLATE/bug_report.md")),
            ("Feature request template", os.path.exists(".github/ISSUE_TEMPLATE/feature_request.md")),
        ],
        "Demo Scripts": [
            ("run_demo.sh", os.path.exists("run_demo.sh")),
            ("run_demo.ps1", os.path.exists("run_demo.ps1")),
            ("run_demo.sh is executable", os.path.exists("run_demo.sh") and os.access("run_demo.sh", os.X_OK)),
        ],
        "Environment Configuration": [
            (".env.example", os.path.exists(".env.example")),
            (".gitignore", os.path.exists(".gitignore")),
            ("backend/.gitignore", os.path.exists("backend/.gitignore")),
            ("frontend/.gitignore", os.path.exists("frontend/.gitignore")),
        ],
        "Test Structure": [
            ("tests directory", os.path.exists("tests")),
            ("tests/backend directory", os.path.exists("tests/backend")),
            ("tests/conftest.py", os.path.exists("tests/conftest.py")),
            ("Unit tests", os.path.exists("tests/backend/unit")),
            ("Integration tests", os.path.exists("tests/backend/integration")),
        ],
        "Task Documentation": [
            ("tasks directory", os.path.exists("tasks")),
            ("Task 1.1", os.path.exists("tasks/task1.1.md")),
            ("Task 1.2", os.path.exists("tasks/task1.2.md")),
            ("Task 1.3", os.path.exists("tasks/task1.3.md")),
            ("All 15 task files", len([f for f in os.listdir("tasks") if f.endswith('.md')]) == 15),
        ],
    }
    
    total_tests = 0
    passed_tests = 0
    
    for category, category_tests in tests.items():
        print(f"\n{category}:")
        print("-" * 40)
        
        for test_name, result in category_tests:
            total_tests += 1
            if result:
                passed_tests += 1
                status = "✅ PASS"
                color = "\033[92m"  # Green
            else:
                status = "❌ FAIL"
                color = "\033[91m"  # Red
            
            reset = "\033[0m"  # Reset color
            print(f"  {color}{status}{reset} - {test_name}")
            test_results.append((test_name, result))
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    print(f"Total Tests: {total_tests}")
    print(f"Passed: {passed_tests}")
    print(f"Failed: {total_tests - passed_tests}")
    print(f"Pass Rate: {(passed_tests/total_tests)*100:.1f}%")
    
    if passed_tests == total_tests:
        print("\n🎉 All tests passed! Project structure is complete.")
    else:
        print(f"\n⚠️  {total_tests - passed_tests} tests failed. Please review the failures above.")
    
    return passed_tests == total_tests


def check_file_content():
    """Additional content verification tests"""
    print("\n" + "=" * 60)
    print("Content Verification Tests")
    print("=" * 60)
    
    content_tests = []
    
    # Check README has badges
    if os.path.exists("README.md"):
        with open("README.md", "r") as f:
            readme_content = f.read()
            has_badges = "![" in readme_content and "badge" in readme_content.lower()
            content_tests.append(("README has badges", has_badges))
            content_tests.append(("README mentions Docker", "docker" in readme_content.lower()))
            content_tests.append(("README has Quick Start", "quick start" in readme_content.lower()))
    
    # Check ROADMAP has completion marker
    if os.path.exists("ROADMAP.md"):
        with open("ROADMAP.md", "r") as f:
            roadmap_content = f.read()
            content_tests.append(("Task 1.1 marked complete", "Task 1.1" in roadmap_content and "✅" in roadmap_content))
    
    # Check CI workflow configuration
    if os.path.exists(".github/workflows/ci.yml"):
        with open(".github/workflows/ci.yml", "r") as f:
            ci_content = f.read()
            content_tests.append(("CI has backend tests", "backend-tests" in ci_content))
            content_tests.append(("CI has linting", "ruff" in ci_content or "lint" in ci_content))
            content_tests.append(("CI has security scan", "security" in ci_content.lower() or "bandit" in ci_content))
    
    # Check Docker Compose services
    if os.path.exists("docker-compose.yml"):
        with open("docker-compose.yml", "r") as f:
            docker_content = f.read()
            content_tests.append(("Docker has postgres service", "postgres:" in docker_content))
            content_tests.append(("Docker has minio service", "minio:" in docker_content))
            content_tests.append(("Docker has backend service", "backend:" in docker_content))
    
    # Display results
    all_passed = True
    for test_name, result in content_tests:
        if result:
            status = "✅ PASS"
            color = "\033[92m"
        else:
            status = "❌ FAIL"
            color = "\033[91m"
            all_passed = False
        
        reset = "\033[0m"
        print(f"  {color}{status}{reset} - {test_name}")
    
    return all_passed


if __name__ == "__main__":
    # Change to project root
    project_root = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_root)
    
    # Run tests
    structure_passed = run_structure_tests()
    content_passed = check_file_content()
    
    # Final result
    print("\n" + "=" * 60)
    if structure_passed and content_passed:
        print("✅ ALL TESTS PASSED - Project structure is complete and valid!")
        sys.exit(0)
    else:
        print("❌ Some tests failed - Please review the failures above")
        sys.exit(1)