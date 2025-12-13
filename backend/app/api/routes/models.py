from fastapi import APIRouter, Query, HTTPException, Request
from typing import Optional, List
from app.services.fal_client import FalAIClient
from app.services.redis import RedisService
from app.models.schema import ModelInfo, ModelCategory, ModelSearchResponse
from app.core.config import get_settings
import logging

router = APIRouter()
logger = logging.getLogger(__name__)
settings = get_settings()

@router.get(
    "/models", 
    response_model=ModelSearchResponse,
    summary="List all available models",
    description="Get a list of all available Fal.ai models with optional filtering"
)
async def list_models(
    request: Request,
    category: Optional[ModelCategory] = Query(None, description="Filter by category"),
    limit: int = Query(50, ge=1, le=100, description="Maximum number of results"),
    offset: int = Query(0, ge=0, description="Offset for pagination")
):
    """
    List all available models

    - **category**: Optional category filter
    - **limit**: Maximum results to return
    - **offset**: Pagination offset
    """
    try:
        redis: RedisService = request.app.state.redis
        cache_key = f"models:list:{category}:{limit}:{offset}"

        # Check cache
        cached = await redis.get(cache_key)
        if cached:
            logger.info("Returning cached model list")
            return cached

        # Get models from Fal.ai client
        fal_client = FalAIClient()
        models = fal_client.search_models(category=category)

        # Apply pagination
        total = len(models)
        paginated_models = models[offset:offset+limit]

        response = {
            "models": paginated_models,
            "total": total,
            "query": None
        }

        # Cache for 1 hour
        await redis.set(cache_key, response, ttl=settings.CACHE_TTL_MODELS)

        return response

    except Exception as e:
        logger.error(f"Error listing models: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get(
    "/models/search",
    response_model=ModelSearchResponse,
    summary="Search models",
    description="Search for models by name, description, or ID"
)
async def search_models(
    request: Request,
    q: str = Query(..., min_length=1, description="Search query"),
    category: Optional[ModelCategory] = Query(None, description="Filter by category"),
    limit: int = Query(20, ge=1, le=100, description="Maximum number of results")
):
    """
    Search for models

    - **q**: Search query (required)
    - **category**: Optional category filter
    - **limit**: Maximum results to return
    """
    try:
        redis: RedisService = request.app.state.redis
        cache_key = f"models:search:{q}:{category}:{limit}"

        # Check cache
        cached = await redis.get(cache_key)
        if cached:
            logger.info("Returning cached search results")
            return cached

        # Search models
        fal_client = FalAIClient()
        models = fal_client.search_models(query=q, category=category)

        # Limit results
        limited_models = models[:limit]

        response = {
            "models": limited_models,
            "total": len(models),
            "query": q
        }

        # Cache for 1 hour
        await redis.set(cache_key, response, ttl=settings.CACHE_TTL_MODELS)

        return response

    except Exception as e:
        logger.error(f"Error searching models: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get(
    "/models/{model_id:path}",
    response_model=ModelInfo,
    summary="Get model details",
    description="Get detailed information about a specific model"
)
async def get_model(
    request: Request,
    model_id: str
):
    """
    Get detailed model information

    - **model_id**: Fal.ai model identifier (e.g., fal-ai/flux/dev)
    """
    try:
        redis: RedisService = request.app.state.redis
        cache_key = f"models:detail:{model_id}"

        # Check cache
        cached = await redis.get(cache_key)
        if cached:
            logger.info("Returning cached model details")
            return cached

        # Get model info
        fal_client = FalAIClient()
        model_info = fal_client.get_model_info(model_id)

        if not model_info:
            raise HTTPException(status_code=404, detail=f"Model {model_id} not found")

        # Cache for 1 hour
        await redis.set(cache_key, model_info, ttl=settings.CACHE_TTL_MODELS)

        return model_info

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting model details: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get(
    "/models/categories/list",
    summary="List model categories",
    description="Get all available model categories"
)
async def list_categories():
    """List all available model categories"""
    try:
        fal_client = FalAIClient()
        categories = fal_client.list_categories()
        return {
            "categories": categories,
            "total": len(categories)
        }
    except Exception as e:
        logger.error(f"Error listing categories: {e}")
        raise HTTPException(status_code=500, detail=str(e))
