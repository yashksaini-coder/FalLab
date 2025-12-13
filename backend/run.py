import uvicorn
from app.core.config import get_settings

settings = get_settings()

if __name__ == "__main__":
    print("Starting server at http://localhost:8000")
    uvicorn.run(
        "app.main:app",
        port=8000,
        reload=settings.DEBUG,
        log_level="info"
    )
