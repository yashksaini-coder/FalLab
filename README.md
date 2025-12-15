<div align="center">

# 🎨 FalLab - AI Image Generation Playground

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)
[![GitHub Stars](https://img.shields.io/github/stars/yashksaini-coder/FalLab?style=social)](https://github.com/yashksaini-coder/FalLab/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/yashksaini-coder/FalLab?style=social)](https://github.com/yashksaini-coder/FalLab/network/members)

**A full-stack web application for exploring and generating AI images using Fal.ai**

[Report Bug](https://github.com/yashksaini-coder/FalLab/issues) · [Request Feature](https://github.com/yashksaini-coder/FalLab/issues)

</div>

---

## 🎯 About The Project

FalLab is a modern, feature-rich web application that provides an intuitive interface to explore AI image generation models from Fal.ai. Users can browse available models, view their details organized by category, and generate stunning AI images with custom prompts and parameters.

**Key Features:**
- 🎨 **Model Discovery** - Browse 50+ AI image generation models organized by category
- ✨ **Interactive Playground** - Generate images with real-time parameter tuning
- 📊 **Model Details** - View comprehensive information about each model including descriptions and thumbnails
- 🔄 **Async Generation** - Queue-based image generation with real-time status polling
- 💾 **Conversation History** - Save and revisit your generation sessions
- 🚀 **High Performance** - Built with modern technologies for lightning-fast response times
- 🔒 **Secure** - Production-ready backend with proper error handling and validation

---

## 🛠️ Tech Stack

### Frontend

<div align="center">

| Technology | Purpose |
|-----------|---------|
| **Next.js 13+** | React framework with App Router and server components |
| **React 18** | UI component library |
| **TypeScript** | Type-safe JavaScript development |
| **TailwindCSS** | Utility-first CSS styling |
| **Shadcn/ui** | High-quality React components |
| **React Hook Form** | Form state management |
| **Zod** | Schema validation |

</div>

### Backend

<div align="center">

| Technology | Purpose |
|-----------|---------|
| **FastAPI** | Modern Python web framework |
| **Python 3.10+** | Server runtime |
| **Celery** | Async task queue for image generation |
| **Redis** | Message broker and caching |
| **Fal.ai SDK** | AI image generation models integration |
| **Pydantic** | Data validation and serialization |

</div>

### DevOps & Deployment

<div align="center">

| Technology | Purpose |
|-----------|---------|
| **Docker** | Container orchestration |
| **Docker Compose** | Multi-container orchestration |
| **Postman** | API testing and documentation |
| **Git** | Version control |

</div>

---

## 📁 Project Structure

```
FalLab/
├── 📂 frontend/                    # Next.js React frontend
│   ├── 📂 app/                     # App Router pages and layouts
│   │   ├── 📂 playground/          # Image generation playground
│   │   ├── 📂 models/              # Models browser page
│   │   └── 📂 health/              # API health check page
│   ├── 📂 components/              # Reusable React components
│   │   ├── 📂 playground/          # Playground-specific components
│   │   └── 📂 ui/                  # Shadcn/ui components
│   ├── 📂 lib/                     # Utilities and API client
│   │   └── api.ts                  # TypeScript API client
│   ├── 📂 styles/                  # Global styles
│   └── 📄 package.json             # Frontend dependencies
│
├── 📂 backend/                     # FastAPI Python backend
│   ├── 📂 app/
│   │   ├── 📂 api/
│   │   │   └── 📂 routes/          # API endpoints
│   │   │       ├── generate.py     # Image generation routes
│   │   │       ├── models.py       # Models listing routes
│   │   │       └── health.py       # Health check endpoint
│   │   ├── 📂 core/
│   │   │   ├── config.py           # Configuration management
│   │   │   └── middleware.py       # CORS & error handling
│   │   ├── 📂 models/
│   │   │   └── schema.py           # Pydantic models/schemas
│   │   ├── 📂 services/
│   │   │   ├── fal_client.py       # Fal.ai SDK wrapper
│   │   │   ├── queue_service.py    # Queue management
│   │   │   └── redis.py            # Redis client
│   │   ├── 📂 workers/
│   │   │   ├── celery_app.py       # Celery app configuration
│   │   │   ├── manager.py          # Worker task manager
│   │   │   └── tasks.py            # Background tasks
│   │   └── main.py                 # FastAPI app initialization
│   ├── 📂 tests/                   # Unit and integration tests
│   ├── requirements.txt            # Python dependencies
│   ├── run.py                      # Development server entry point
│   ├── worker.sh                   # Celery worker startup script
│   ├── Dockerfile                  # Container image definition
│   └── docker-compose.yml          # Multi-container orchestration
│
├── 📄 README.md                    # This file
├── 📄 CONTRIBUTING.md              # Contribution guidelines
└── 📄 LICENSE                      # MIT License
```

---

## 🚀 Getting Started

### Prerequisites

- **Node.js** 18+ and npm/bun
- **Python** 3.10+
- **Docker & Docker Compose** (for containerized setup)
- **Fal.ai API Key** (free tier available at [fal.ai](https://fal.ai))
- **Redis** (automatically set up with Docker)

### Installation

#### 1. Clone the Repository

```bash
git clone https://github.com/yashksaini-coder/FalLab.git
cd FalLab
```

#### 2. Backend Setup

```bash
cd backend

# Create Python virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.local .env

# Add your Fal.ai API key
echo "FAL_KEY=your_api_key_here" >> .env
```

#### 3. Frontend Setup

```bash
cd ../frontend

# Install dependencies
npm install
# or
bun install

# Create .env.local if needed
# The frontend automatically connects to http://localhost:8000
```

#### 4. Run with Docker Compose (Recommended)

```bash
cd backend

# Start all services (FastAPI, Redis, Celery workers)
docker-compose up --build

# In another terminal, start the frontend
cd ../frontend
npm run dev
```

#### 5. Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

### Manual Development Setup

**Terminal 1 - Backend:**
```bash
cd backend
python run.py
```

**Terminal 2 - Celery Worker:**
```bash
cd backend
celery -A app.workers.celery_app worker --loglevel=info
```

**Terminal 3 - Frontend:**
```bash
cd frontend
npm run dev
```

---

## 📖 API Documentation

### Base URL
```
http://localhost:8000/api/v1
```

### Key Endpoints

#### Get Available Models
```http
GET /models?limit=50&offset=0
```

**Response:**
```json
{
  "models": [
    {
      "endpoint_id": "fal-ai/flux/dev",
      "metadata": {
        "display_name": "Flux Dev",
        "category": "text-to-image",
        "description": "Fast and accurate text-to-image generation",
        "thumbnail_url": "..."
      }
    }
  ]
}
```

#### Get Model Categories
```http
GET /models/categories
```

**Response:**
```json
{
  "categories": ["text-to-image", "image-to-image", "inpainting", "upscaling"]
}
```

#### Submit Generation Request
```http
POST /generate
Content-Type: application/json

{
  "model_id": "fal-ai/flux/dev",
  "prompt": "A serene mountain landscape at sunset",
  "parameters": {}
}
```

**Response:**
```json
{
  "request_id": "req_12345",
  "status": "queued",
  "created_at": "2025-12-15T10:30:00Z"
}
```

#### Check Generation Status
```http
GET /status/{request_id}
```

**Response:**
```json
{
  "request_id": "req_12345",
  "status": "completed",
  "result": {
    "images": [
      {
        "url": "https://...",
        "size": "1024x1024"
      }
    ]
  }
}
```

#### Health Check
```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "backend": "connected",
  "redis": "connected",
  "fal_api": "configured"
}
```

---

## 🎮 Usage Guide

### 1. Browse Models
- Navigate to `/models` page
- Filter by category using the left sidebar
- Search for specific models
- Click on any model to view full details

### 2. Generate Images
- Go to `/playground`
- Select a model from the dropdown
- Enter your prompt describing the image you want
- Click "Generate"
- Watch real-time status updates
- Your generated image appears in the conversation

### 3. View Generation History
- All generated images are saved in your conversation history
- Switch between different chats using the sidebar
- Export conversation history (coming soon)

---

## 🔧 Configuration

### Environment Variables

**Root `.env` (Recommended for Docker/Cloud):**
```env
FAL_API_KEY=your_fal_api_key
DEBUG=True
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_DB=0
REDIS_PASSWORD=
FAL_API_BASE_URL=https://fal.run
FAL_API_TIMEOUT=300
CORS_ORIGINS=http://localhost:3000,http://frontend:3000
API_V1_PREFIX=/api/v1
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
API_URL=http://localhost:8000/api/v1
NODE_ENV=production
```

**Frontend (Vercel):**
- Set `NEXT_PUBLIC_API_URL` in the Vercel dashboard to your backend’s public URL.

**Backend (DigitalOcean):**
- Set all backend-related variables in the App Platform dashboard or pass them via `.env` on a Droplet.

---

## 🚀 Docker & Cloud Deployment

### 1. Unified Environment Configuration

- Place a single `.env` file at the project root (see below for example). Docker Compose and most cloud platforms will pick this up automatically.
- Example `.env`:
  ```env
  # Backend
  FAL_API_KEY=your_fal_api_key
  DEBUG=True
  REDIS_HOST=redis
  REDIS_PORT=6379
  REDIS_DB=0
  REDIS_PASSWORD=
  FAL_API_BASE_URL=https://fal.run
  FAL_API_TIMEOUT=300
  CORS_ORIGINS=http://localhost:3000,http://frontend:3000
  API_V1_PREFIX=/api/v1
  # Frontend
  NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
  API_URL=http://localhost:8000/api/v1
  NODE_ENV=production
  ```

### 2. Local Docker Compose (All-in-One)

```bash
# From the project root
cd backend
# Build and start all services (backend, worker, redis, frontend)
docker-compose up --build
```
- Access the frontend at [http://localhost:3000](http://localhost:3000)
- Access the backend API at [http://localhost:8000](http://localhost:8000)

### 3. Deploy Backend to DigitalOcean (App Platform or Droplet)

#### **A. DigitalOcean App Platform (Recommended)**
1. Push your repo to GitHub.
2. In DigitalOcean, create a new App and connect your repo.
3. Add two services:
   - **Backend API**: Use `/backend` as context, Dockerfile as `backend/Dockerfile`.
   - **Worker**: Use `/backend` as context, Dockerfile as `backend/Dockerfile.worker`.
4. Add a database component for Redis or use the built-in Redis service.
5. Set environment variables in the App Platform dashboard (copy from your `.env`).
6. Expose port 8000 for the backend service.
7. Deploy!

#### **B. DigitalOcean Droplet (VM)**
1. SSH into your Droplet.
2. Clone your repo and copy your `.env` to the root.
3. Run:
   ```bash
   cd backend
   docker-compose up -d --build
   ```
4. Set up a reverse proxy (e.g., Nginx) for HTTPS and custom domains if needed.

### 4. Deploy Frontend to Vercel

1. Push your frontend code to GitHub (in the `frontend/` directory).
2. Go to [Vercel](https://vercel.com/) and import your repo.
3. Set the project root to `frontend/`.
4. In Vercel dashboard, set the environment variable:
   - `NEXT_PUBLIC_API_URL` = `https://<your-backend-domain>/api/v1`
5. Deploy!

**Note:**
- For local development, `NEXT_PUBLIC_API_URL` can be `http://localhost:8000/api/v1`.
- For production, set it to your DigitalOcean backend’s public URL.

---

## 🛰️ Production Checklist
- [ ] Set all secrets and API keys in your cloud provider’s dashboard.
- [ ] Use HTTPS for all public endpoints (DigitalOcean App Platform and Vercel handle this automatically).
- [ ] Monitor logs and health endpoints (`/api/v1/health`).
- [ ] Scale worker and backend services as needed for load.

---

## 🧪 Testing

### Run Backend Tests
```bash
cd backend
pytest tests/
```

### API Testing with Postman
- Import `backend/FalLab_API_Collection.postman_collection.json` in Postman
- Use `backend/FalLab_API_Environment.postman_environment.json` for environment variables
- Run the collection to test all endpoints

---

## 📦 Project Statistics

- **Frontend**: ~15KB TypeScript/React components
- **Backend**: FastAPI with async support
- **Models**: 50+ AI image generation models
- **Database**: Redis-backed queue system
- **Response Time**: <100ms API latency
- **Async Processing**: Queue-based image generation with WebSocket polling

---

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

### Quick Start for Contributors

1. Fork the repository
2. Create a feature branch: `git checkout -b feat/amazing-feature`
3. Commit your changes: `git commit -m 'Add amazing feature'`
4. Push to the branch: `git push origin feat/amazing-feature`
5. Open a Pull Request

---

## 🐛 Troubleshooting

### Issue: 403 Error from Fal.ai
**Solution:** Ensure your `FAL_KEY` is set in the backend `.env` file
```bash
echo "FAL_KEY=your_key" >> backend/.env
docker-compose restart
```

### Issue: Frontend can't connect to backend
**Solution:** Verify backend is running on port 8000
```bash
curl http://localhost:8000/api/v1/health
```

### Issue: Redis connection failed
**Solution:** Restart Docker containers
```bash
docker-compose down
docker-compose up --build
```

### Issue: Models not showing up
**Solution:** Check Fal.ai API key and network connectivity
```bash
curl http://localhost:8000/api/v1/models?limit=5
```

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

---

## 💖 Support

If you find FalLab helpful, please consider:

<div align="center">

[![Star on GitHub](https://img.shields.io/badge/⭐%20Star%20this%20repo-GitHub-brightgreen?style=for-the-badge)](https://github.com/yashksaini-coder/FalLab)
[![Buy Me A Coffee](https://img.shields.io/badge/☕%20Buy%20Me%20A%20Coffee-Support-yellow?style=for-the-badge&logo=buy-me-a-coffee)](https://buymeacoffee.com/yashksaini)
[![Report Issues](https://img.shields.io/badge/🐛%20Report%20Issues-GitHub-red?style=for-the-badge)](https://github.com/yashksaini-coder/FalLab/issues)

</div>

---

<div align="center">

Made with ❤️ by [Yash K. Saini](https://github.com/yashksaini-coder)

[![Portfolio](https://img.shields.io/badge/Portfolio-Visit-blue?style=flat&logo=google-chrome)](https://www.yashksaini.systems/)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Follow-blue?style=flat&logo=linkedin)](https://www.linkedin.com/in/yashksaini/)
[![Twitter](https://img.shields.io/badge/Twitter-Follow-blue?style=flat&logo=x)](https://x.com/0xCracked_dev)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-black?style=flat&logo=github)](https://github.com/yashksaini-coder)

</div>