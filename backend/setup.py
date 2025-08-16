"""
Setup configuration for OSSGameForge backend
"""

from setuptools import find_packages, setup

setup(
    name="ossgameforge-backend",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    python_requires=">=3.9",
    install_requires=[
        "fastapi>=0.109.0",
        "uvicorn>=0.26.0",
        "pydantic>=2.5.0",
        "sqlalchemy>=2.0.0",
        "alembic>=1.13.1",
        "psycopg2-binary>=2.9.9",
        "python-multipart>=0.0.6",
        "minio>=7.2.2",
        "pillow>=10.2.0",
        "python-jose>=3.3.0",
        "passlib>=1.7.4",
        "tinytag>=1.10.1",
    ],
)
