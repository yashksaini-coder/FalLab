from fastapi import APIRouter, Query, HTTPException, Request
from typing import Optional, List
from app.services.fal_client import FalAIClient
from app.services.redis import RedisService
from app.models.schema import ModelInfo, ModelsListResponse
from app.core.config import get_settings
import logging
import json

router = APIRouter()
logger = logging.getLogger(__name__)
settings = get_settings()


def serialize_models(models: List[dict]) -> List[dict]:
    """Convert model dicts to JSON-serializable format"""
    return json.loads(json.dumps(models, default=str))


@router.post(
    "/models/refresh",
    summary="Refresh models cache",
    description="Fetch and refresh the models list from Fal.ai API"
)
async def refresh_models(request: Request):
    """
    Force refresh the models cache from Fal.ai

    This endpoint fetches the latest models list from the Fal.ai API
    and caches it. Useful for keeping the cache up-to-date.
    """
    try:
        redis: RedisService = request.app.state.redis
        fal_client = FalAIClient(api_key=settings.FAL_API_KEY)

        # Fetch fresh models from Fal.ai API
        models = await fal_client._get_models_list()

        # Cache the models
        cache_key = "fal:models:all"
        await redis.set(cache_key, serialize_models(models), ttl=settings.CACHE_TTL_MODELS)

        logger.info(f"Models cache refreshed with {len(models)} models")
        return {
            "status": "success",
            "total_models": len(models),
            "message": f"Successfully loaded {len(models)} models from Fal.ai"
        }
    except Exception as e:
        logger.error(f"Error refreshing models: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to refresh models: {str(e)}")


@router.get(
    "/models",
    summary="List all available models",
    description="Get a list of all available Fal.ai models with optional filtering"
)
async def list_models(
    request: Request,
    category: Optional[str] = Query(None, description="Filter by category (e.g., text-to-image)"),
    limit: int = Query(50, ge=1, le=100, description="Maximum number of results"),
    skip: int = Query(0, ge=0, description="Number of results to skip for pagination")
):
    """
    List all available models

    - **category**: Optional category filter
    - **limit**: Maximum results to return (1-100)
    - **skip**: Number of results to skip for pagination

    Returns paginated list of models with their metadata.
    """
    try:
        redis: RedisService = request.app.state.redis
        cache_key = "fal:models:all"

        # Try to get from cache first
        cached_models = await redis.get(cache_key)

        if not cached_models:
            # Fetch from Fal.ai API
            fal_client = FalAIClient(api_key=settings.FAL_API_KEY)
            models = await fal_client._get_models_list()

            if not models:
                raise Exception("No models returned from Fal.ai API")

            # Cache for future requests
            await redis.set(cache_key, serialize_models(models), ttl=settings.CACHE_TTL_MODELS)
            logger.info(f"Fetched {len(models)} models from API and cached")
        else:
            models = cached_models
            logger.debug("Using cached models list")

        # Filter by category if provided
        if category:
            fal_client = FalAIClient(api_key=settings.FAL_API_KEY)
            models = fal_client.get_models_by_category(models, category)
            logger.info(f"Filtered to {len(models)} models in category '{category}'")

        # Apply pagination
        total = len(models)
        paginated_models = models[skip : skip + limit]

        response = {
            "models": serialize_models(paginated_models),
            "total": total,
            "next_cursor": None  # Could implement cursor-based pagination here
        }

        logger.info(f"Listed {len(paginated_models)} of {total} models (category={category}, skip={skip})")
        return response

    except Exception as e:
        logger.error(f"Error listing models: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to list models: {str(e)}")


@router.get(
    "/models/search",
    summary="Search models",
    description="Search for models by endpoint_id, display_name, description, or tags"
)
async def search_models(
    request: Request,
    q: str = Query(..., min_length=1, description="Search query"),
    limit: int = Query(20, ge=1, le=100, description="Maximum number of results")
):
    """
    Search for models

    Searches across:
    - endpoint_id (highest priority)
    - metadata.display_name
    - metadata.description
    - metadata.tags

    - **q**: Search query (required)
    - **limit**: Maximum results to return (1-100)

    Returns matching models sorted by relevance.
    """
    try:
        redis: RedisService = request.app.state.redis
        cache_key = f"fal:models:search:{q.lower()}:{limit}"

        # Try cache first
        cached_results = await redis.get(cache_key)
        if cached_results:
            logger.debug(f"Returning cached search results for: {q}")
            return {"models": cached_results, "total": len(cached_results), "query": q}

        # Get all models
        cache_key_all = "fal:models:all"
        cached_models = await redis.get(cache_key_all)

        if not cached_models:
            # Fetch from API
            fal_client = FalAIClient(api_key=settings.FAL_API_KEY)
            models = await fal_client._get_models_list()
            if not models:
                raise Exception("No models available")
            await redis.set(cache_key_all, serialize_models(models), ttl=settings.CACHE_TTL_MODELS)
        else:
            models = cached_models

        # Perform search
        fal_client = FalAIClient(api_key=settings.FAL_API_KEY)
        results = fal_client.search_models(query=q, models=models, limit=limit)

        # Cache search results
        await redis.set(cache_key, serialize_models(results), ttl=3600)  # 1 hour

        response = {"models": serialize_models(results), "total": len(results), "query": q}

        logger.info(f"Search for '{q}' found {len(results)} results")
        return response

    except Exception as e:
        logger.error(f"Error searching models: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")


@router.get(
    "/models/categories",
    summary="List model categories",
    description="Get all available model categories"
)
async def list_categories(request: Request):
    """
    List all available model categories

    Returns a sorted list of all unique categories available in the Fal.ai catalog.
    """
    try:
        redis: RedisService = request.app.state.redis
        cache_key = "fal:models:categories"

        # Try cache
        cached_categories = await redis.get(cache_key)
        if cached_categories:
            logger.debug("Returning cached categories")
            return {"categories": cached_categories, "total": len(cached_categories)}

        # Get all models first
        cache_key_all = "fal:models:all"
        cached_models = await redis.get(cache_key_all)

        if not cached_models:
            fal_client = FalAIClient(api_key=settings.FAL_API_KEY)
            models = await fal_client._get_models_list()
            if not models:
                raise Exception("No models available")
            await redis.set(cache_key_all, serialize_models(models), ttl=settings.CACHE_TTL_MODELS)
        else:
            models = cached_models

        # Extract categories
        fal_client = FalAIClient(api_key=settings.FAL_API_KEY)
        categories = fal_client.get_categories(models)

        # Cache categories
        await redis.set(cache_key, categories, ttl=settings.CACHE_TTL_MODELS)

        logger.info(f"Listed {len(categories)} unique categories")
        return {"categories": categories, "total": len(categories)}

    except Exception as e:
        logger.error(f"Error listing categories: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to list categories: {str(e)}")


@router.get(
    "/models/{model_id:path}",
    summary="Get model details",
    description="Get detailed information about a specific model"
)
async def get_model(request: Request, model_id: str):
    """
    Get detailed model information

    - **model_id**: Fal.ai model endpoint_id (e.g., fal-ai/flux/dev)

    Returns complete model information including metadata, description, tags, etc.
    """
    try:
        redis: RedisService = request.app.state.redis
        cache_key = f"fal:models:detail:{model_id}"

        # Check cache first
        cached_model = await redis.get(cache_key)
        if cached_model:
            logger.debug(f"Returning cached model details for: {model_id}")
            return cached_model

        # Get all models
        cache_key_all = "fal:models:all"
        cached_models = await redis.get(cache_key_all)

        if not cached_models:
            fal_client = FalAIClient(api_key=settings.FAL_API_KEY)
            models = await fal_client._get_models_list()
            if not models:
                raise Exception("No models available")
            await redis.set(cache_key_all, serialize_models(models), ttl=settings.CACHE_TTL_MODELS)
        else:
            models = cached_models

        # Find model
        fal_client = FalAIClient(api_key=settings.FAL_API_KEY)
        model_info = fal_client.get_model_info(endpoint_id=model_id, models=models)

        if not model_info:
            logger.warning(f"Model not found: {model_id}")
            raise HTTPException(status_code=404, detail=f"Model '{model_id}' not found")

        # Cache model details
        await redis.set(cache_key, serialize_models([model_info]), ttl=settings.CACHE_TTL_MODELS)

        logger.info(f"Retrieved model details for: {model_id}")
        return serialize_models([model_info])[0]

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting model details: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to get model details: {str(e)}")
