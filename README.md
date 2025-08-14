# OSSGameForge: The AI-Powered Game Creation Suite

[![CI/CD Pipeline](https://github.com/ClayKa/oss-game-forge/actions/workflows/ci.yml/badge.svg)](https://github.com/ClayKa/oss-game-forge/actions/workflows/ci.yml)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109.2-009688.svg)](https://fastapi.tiangolo.com)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v2.json)](https://github.com/charliermarsh/ruff)

## 🎮 Overview

OSSGameForge is an innovative AI-powered game creation suite designed for rapid prototyping and game development. Upload your assets, describe your vision, and let AI generate playable game scenes that can be exported to multiple formats.

### ✨ Key Features

- **🎨 Asset Upload with Privacy**: Secure asset management with mandatory consent validation and automatic EXIF stripping
- **🤖 AI-Powered Generation**: Intelligent scene generation with robust fallback mechanisms
- **👁️ Real-time Preview**: Interactive viewer for immediate scene visualization
- **📦 Universal Export**: Export to HTML5 runner packages that work everywhere
- **🔒 Enterprise-Grade Security**: Built-in security scanning, dependency checks, and data sanitization
- **🚀 Production-Ready**: Comprehensive CI/CD, testing, and monitoring

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose
- Git
- Python 3.10+ (for local development)
- Node.js 18+ (for frontend development)

### One-Click Demo

#### Linux/macOS
```bash
git clone https://github.com/ClayKa/oss-game-forge.git
cd oss-game-forge
./run_demo.sh
```

#### Windows PowerShell
```powershell
git clone https://github.com/ClayKa/oss-game-forge.git
cd oss-game-forge
.\run_demo.ps1
```

The application will be available at:
- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **MinIO Console**: http://localhost:9001

### Standard Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/ClayKa/oss-game-forge.git
   cd oss-game-forge
   ```

2. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Start services**
   ```bash
   docker-compose up --build -d
   ```

4. **Verify installation**
   ```bash
   curl http://localhost:8000/health
   ```

## 🏗️ Architecture

```
oss-game-forge/
├── backend/          # FastAPI backend
│   └── app/
│       ├── routers/     # API endpoints
│       ├── services/    # Business logic
│       ├── models/      # Database models
│       └── schemas/     # Pydantic schemas
├── frontend/         # React frontend
│   └── src/
│       ├── components/  # UI components
│       ├── pages/       # Page components
│       └── services/    # API clients
├── devops/          # Infrastructure
│   ├── docker/         # Docker configs
│   └── mocks/          # Mock data
└── tests/           # Test suites
    ├── backend/        # Backend tests
    └── e2e/            # End-to-end tests
```

## 🔧 Development

### Backend Development

```bash
# Install dependencies
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements-dev.txt

# Run linting
ruff check .
black --check .

# Run tests
pytest tests/ --cov=app

# Start development server
uvicorn app.main:app --reload
```

### Frontend Development

```bash
# Install dependencies
cd frontend
npm install

# Start development server
npm run dev

# Run tests
npm test

# Build for production
npm run build
```

### Pre-commit Hooks

```bash
# Install pre-commit hooks
pre-commit install

# Run manually
pre-commit run --all-files
```

## 📚 API Documentation

### Core Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check |
| `/api/assets` | POST | Upload asset with consent |
| `/api/generation` | POST | Generate game scene |
| `/api/export` | POST | Export scene package |

### Example: Upload Asset

```bash
curl -X POST http://localhost:8000/api/assets \
  -F "file=@image.png" \
  -F "project_id=proj-123" \
  -F "user_consent=true"
```

### Example: Generate Scene

```bash
curl -X POST http://localhost:8000/api/generation \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Create a platformer level with floating islands",
    "project_id": "proj-123"
  }'
```

## 🧪 Testing

### Run All Tests
```bash
# Backend tests
pytest tests/backend --cov

# Frontend tests
npm test

# E2E tests
npm run test:e2e
```

### Golden Sample Tests

The project includes 3 golden samples for validation:
1. **Simple Geometry**: Core rendering logic
2. **Asset Intensive**: Asset loading and pathing
3. **Complex Structure**: JSON parsing and recursion

## 🚢 Deployment

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `MOCK_MODE` | Enable mock responses | `false` |
| `USE_LOCAL_MODEL` | Use local AI model | `false` |
| `DATABASE_URL` | PostgreSQL connection | See .env.example |
| `MINIO_ENDPOINT` | MinIO server | `localhost:9000` |

### Production Checklist

- [ ] Update all secrets in `.env`
- [ ] Enable HTTPS/TLS
- [ ] Configure firewall rules
- [ ] Set up monitoring (Prometheus/Grafana)
- [ ] Configure backups
- [ ] Review security settings
- [ ] Load test the API

## 📊 Performance

| Mode | Latency | Requirements |
|------|---------|--------------|
| **Fallback Mode** | Instant | No GPU required |
| **Local Model** | 15-45s | GPU with ≥16GB VRAM |
| **Cloud Model** | 5-15s | API key required |

## 🔒 Security

- **Consent Management**: Mandatory user consent for all uploads
- **Data Sanitization**: Automatic EXIF stripping for images
- **Dependency Scanning**: Automated security checks in CI
- **Access Control**: Role-based permissions (coming soon)
- **Audit Logging**: Complete generation history tracking

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'feat: add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- FastAPI for the amazing web framework
- The open-source community for invaluable tools and libraries
- All contributors and testers

## 📞 Support

- **Documentation**: [https://docs.ossgameforge.dev](https://docs.ossgameforge.dev)
- **Issues**: [GitHub Issues](https://github.com/ClayKa/oss-game-forge/issues)
- **Discussions**: [GitHub Discussions](https://github.com/ClayKa/oss-game-forge/discussions)

---

Built with ❤️ by the OSSGameForge Team