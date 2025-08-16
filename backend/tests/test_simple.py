"""
Simple tests that don't require external dependencies
"""
import os
import sys

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))


class TestProjectStructure:
    """Test project structure and files exist"""

    def test_backend_directory_exists(self):
        """Test backend directory exists"""
        backend_path = os.path.join(os.path.dirname(__file__), '..', 'backend')
        assert os.path.exists(backend_path)
        assert os.path.isdir(backend_path)

    def test_frontend_directory_exists(self):
        """Test frontend directory exists"""
        frontend_path = os.path.join(os.path.dirname(__file__), '..', 'frontend')
        assert os.path.exists(frontend_path)
        assert os.path.isdir(frontend_path)

    def test_docker_compose_exists(self):
        """Test docker-compose.yml exists"""
        docker_compose_path = os.path.join(os.path.dirname(__file__), '..', 'docker-compose.yml')
        assert os.path.exists(docker_compose_path)
        assert os.path.isfile(docker_compose_path)

    def test_requirements_files_exist(self):
        """Test requirements files exist"""
        req_path = os.path.join(os.path.dirname(__file__), '..', 'backend', 'requirements.txt')
        req_dev_path = os.path.join(os.path.dirname(__file__), '..', 'backend', 'requirements-dev.txt')

        assert os.path.exists(req_path)
        assert os.path.exists(req_dev_path)

    def test_gitignore_exists(self):
        """Test .gitignore files exist"""
        root_gitignore = os.path.join(os.path.dirname(__file__), '..', '.gitignore')
        backend_gitignore = os.path.join(os.path.dirname(__file__), '..', 'backend', '.gitignore')
        frontend_gitignore = os.path.join(os.path.dirname(__file__), '..', 'frontend', '.gitignore')

        assert os.path.exists(root_gitignore)
        assert os.path.exists(backend_gitignore)
        assert os.path.exists(frontend_gitignore)

    def test_ci_workflow_exists(self):
        """Test CI workflow file exists"""
        ci_path = os.path.join(os.path.dirname(__file__), '..', '.github', 'workflows', 'ci.yml')
        assert os.path.exists(ci_path)
        assert os.path.isfile(ci_path)

    def test_readme_exists(self):
        """Test README.md exists"""
        readme_path = os.path.join(os.path.dirname(__file__), '..', 'README.md')
        assert os.path.exists(readme_path)

        # Check it has content
        with open(readme_path) as f:
            content = f.read()
            assert len(content) > 100
            assert 'OSSGameForge' in content

    def test_license_exists(self):
        """Test LICENSE file exists"""
        license_path = os.path.join(os.path.dirname(__file__), '..', 'LICENSE')
        assert os.path.exists(license_path)

        # Check it's MIT license
        with open(license_path) as f:
            content = f.read()
            assert 'MIT License' in content

    def test_demo_scripts_exist(self):
        """Test demo scripts exist"""
        demo_sh = os.path.join(os.path.dirname(__file__), '..', 'run_demo.sh')
        demo_ps1 = os.path.join(os.path.dirname(__file__), '..', 'run_demo.ps1')

        assert os.path.exists(demo_sh)
        assert os.path.exists(demo_ps1)

        # Check shell script is executable
        assert os.access(demo_sh, os.X_OK)

    def test_makefile_exists(self):
        """Test Makefile exists"""
        makefile_path = os.path.join(os.path.dirname(__file__), '..', 'Makefile')
        assert os.path.exists(makefile_path)

        # Check it has common targets
        with open(makefile_path) as f:
            content = f.read()
            assert 'test:' in content
            assert 'lint:' in content
            assert 'build:' in content

    def test_pre_commit_config_exists(self):
        """Test pre-commit configuration exists"""
        pre_commit_path = os.path.join(os.path.dirname(__file__), '..', '.pre-commit-config.yaml')
        assert os.path.exists(pre_commit_path)

    def test_pyproject_toml_exists(self):
        """Test pyproject.toml exists"""
        pyproject_path = os.path.join(os.path.dirname(__file__), '..', 'pyproject.toml')
        assert os.path.exists(pyproject_path)

        # Check it has tool configurations
        with open(pyproject_path) as f:
            content = f.read()
            assert '[tool.ruff]' in content
            assert '[tool.black]' in content
            assert '[tool.pytest.ini_options]' in content


class TestBackendStructure:
    """Test backend code structure"""

    def test_main_app_file_exists(self):
        """Test main.py exists"""
        main_path = os.path.join(os.path.dirname(__file__), '..', 'backend', 'app', 'main.py')
        assert os.path.exists(main_path)

    def test_config_file_exists(self):
        """Test config.py exists"""
        config_path = os.path.join(os.path.dirname(__file__), '..', 'backend', 'app', 'config.py')
        assert os.path.exists(config_path)

    def test_database_file_exists(self):
        """Test database.py exists"""
        db_path = os.path.join(os.path.dirname(__file__), '..', 'backend', 'app', 'database.py')
        assert os.path.exists(db_path)

    def test_dockerfile_exists(self):
        """Test Dockerfile exists"""
        dockerfile_path = os.path.join(os.path.dirname(__file__), '..', 'backend', 'Dockerfile')
        assert os.path.exists(dockerfile_path)

    def test_init_files_exist(self):
        """Test __init__.py files exist in packages"""
        app_init = os.path.join(os.path.dirname(__file__), '..', 'backend', 'app', '__init__.py')
        routers_init = os.path.join(os.path.dirname(__file__), '..', 'backend', 'app', 'routers', '__init__.py')
        services_init = os.path.join(os.path.dirname(__file__), '..', 'backend', 'app', 'services', '__init__.py')

        assert os.path.exists(app_init)
        assert os.path.exists(routers_init)
        assert os.path.exists(services_init)


class TestDocumentation:
    """Test documentation files"""

    def test_contributing_guide_exists(self):
        """Test CONTRIBUTING.md exists"""
        contributing_path = os.path.join(os.path.dirname(__file__), '..', 'CONTRIBUTING.md')
        assert os.path.exists(contributing_path)

        # Check it has sections
        with open(contributing_path) as f:
            content = f.read()
            assert 'How Can I Contribute' in content
            assert 'Pull Requests' in content

    def test_claude_md_exists(self):
        """Test CLAUDE.md exists"""
        claude_path = os.path.join(os.path.dirname(__file__), '..', 'CLAUDE.md')
        assert os.path.exists(claude_path)

        # Check it has Claude-specific content
        with open(claude_path) as f:
            content = f.read()
            assert 'Claude Code' in content
            assert 'Project Overview' in content

    def test_roadmap_exists(self):
        """Test ROADMAP.md exists"""
        roadmap_path = os.path.join(os.path.dirname(__file__), '..', 'ROADMAP.md')
        assert os.path.exists(roadmap_path)

        # Check it has task information
        with open(roadmap_path) as f:
            content = f.read()
            assert 'Task 1.1' in content
            assert '✅' in content  # Task 1.1 should be marked as complete

    def test_github_templates_exist(self):
        """Test GitHub templates exist"""
        pr_template = os.path.join(os.path.dirname(__file__), '..', '.github', 'pull_request_template.md')
        bug_template = os.path.join(os.path.dirname(__file__), '..', '.github', 'ISSUE_TEMPLATE', 'bug_report.md')
        feature_template = os.path.join(os.path.dirname(__file__), '..', '.github', 'ISSUE_TEMPLATE', 'feature_request.md')

        assert os.path.exists(pr_template)
        assert os.path.exists(bug_template)
        assert os.path.exists(feature_template)


class TestEnvironmentFiles:
    """Test environment configuration files"""

    def test_env_example_exists(self):
        """Test .env.example exists"""
        env_example_path = os.path.join(os.path.dirname(__file__), '..', '.env.example')
        assert os.path.exists(env_example_path)

        # Check it has necessary variables
        with open(env_example_path) as f:
            content = f.read()
            assert 'DATABASE_URL' in content
            assert 'MINIO_ENDPOINT' in content
            assert 'MOCK_MODE' in content


class TestTaskFiles:
    """Test task documentation files"""

    def test_all_task_files_exist(self):
        """Test all task files exist"""
        tasks_dir = os.path.join(os.path.dirname(__file__), '..', 'tasks')

        expected_tasks = [
            'task1.1.md', 'task1.2.md', 'task1.3.md',
            'task2.1.md', 'task2.2.md', 'task2.3.md',
            'task3.1&3.2.md', 'task3.3.md',
            'task4.1.md', 'task4.2.md', 'task4.3.md', 'task4.4.md',
            'task5.1.md', 'task5.2.md', 'task5.3.md'
        ]

        for task_file in expected_tasks:
            task_path = os.path.join(tasks_dir, task_file)
            assert os.path.exists(task_path), f"Missing task file: {task_file}"
