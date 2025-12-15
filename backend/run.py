import uvicorn
from app.core.config import get_settings
from app.main import app  # <-- Add this line to export app

settings = get_settings()

if __name__ == "__main__":
    print("Starting server at http://0.0.0.0:8000")
    uvicorn.run(
        "app.main:app",
        # host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level="info"
    )
