Run PYTHONPATH=backend pytest backend/tests \
  
/opt/hostedtoolcache/Python/3.10.18/x64/lib/python3.10/site-packages/_pytest/config/__init__.py:331: PluggyTeardownRaisedWarning: A plugin raised an exception during an old-style hookwrapper teardown.
Plugin: helpconfig, Hook: pytest_cmdline_parse
ConftestImportFailure: ModuleNotFoundError: No module named 'app.models' (from /home/runner/work/oss-game-forge/oss-game-forge/backend/tests/conftest.py)
For more information see https://pluggy.readthedocs.io/en/stable/api_reference.html#pluggy.PluggyTeardownRaisedWarning
  config = pluginmanager.hook.pytest_cmdline_parse(
ImportError while loading conftest '/home/runner/work/oss-game-forge/oss-game-forge/backend/tests/conftest.py'.
backend/tests/conftest.py:21: in <module>
    from app.main import app
backend/app/main.py:14: in <module>
    from .routers import assets, export, generation, health, projects
backend/app/routers/assets.py:25: in <module>
    from ..services import asset_service
backend/app/services/__init__.py:5: in <module>
    from . import asset_service, context_builder, inference_client, postprocessor
backend/app/services/asset_service.py:23: in <module>
    from ..models import Asset
E   ModuleNotFoundError: No module named 'app.models'
Error: Process completed with exit code 4.