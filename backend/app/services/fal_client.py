from typing import Dict, Any, List, Optional
from tenacity import retry, stop_after_attempt, wait_exponential
import logging
import asyncio
from fal_client import SyncClient, AsyncClient
from app.core.config import get_settings
from app.models.schema import ModelCategory

logger = logging.getLogger(__name__)
settings = get_settings()

class FalAIClient:
    """
    Fal.ai API client with retry logic and error handling
    Uses the official fal-client library for better integration
    """

    def __init__(self):
        self.api_key = settings.FAL_API_KEY
        self.timeout = settings.FAL_API_TIMEOUT
        
        # Initialize Fal.ai clients
        # Use SyncClient for synchronous operations (wrapped in async)
        self.sync_client = SyncClient(
            key=self.api_key,
            default_timeout=self.timeout
        )
        
        # Use AsyncClient for async operations
        self.async_client = AsyncClient(
            key=self.api_key,
            default_timeout=self.timeout
        )
        
        # Cache for model metadata
        self._model_cache: Optional[List[Dict[str, Any]]] = None

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10)
    )
    async def submit_request(
        self,
        model_id: str,
        input_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Submit generation request to Fal.ai using queue API

        Args:
            model_id: Fal.ai model identifier
            input_data: Input parameters for the model

        Returns:
            Response containing request_id and status URL
        """
        try:
            logger.info(f"Submitting request to Fal.ai model: {model_id}")
            
            # Use async client for async operations
            # subscribe(application, arguments, ...)
            result = await self.async_client.subscribe(
                model_id,
                input_data
            )
            
            logger.info(f"Request submitted successfully")
            return result

        except Exception as e:
            logger.error(f"Failed to submit request to Fal.ai: {e}", exc_info=True)
            raise Exception(f"Fal.ai API error: {str(e)}")

    async def generate_sync(
        self,
        model_id: str,
        input_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Submit and wait for completion (synchronous generation)
        Uses fal-client's run method for async execution

        Args:
            model_id: Fal.ai model identifier
            input_data: Input parameters

        Returns:
            Final generation result
        """
        try:
            logger.info(f"Running synchronous generation for model: {model_id}")
            
            # Use async client's run method
            # run(application, arguments, ...)
            result = await self.async_client.run(
                model_id,
                input_data,
                timeout=self.timeout
            )
            
            logger.info(f"Generation completed successfully for model: {model_id}")
            return result

        except Exception as e:
            logger.error(f"Generation failed: {e}", exc_info=True)
            raise Exception(f"Generation failed: {str(e)}")

    def _get_all_models(self) -> List[Dict[str, Any]]:
        """
        Get all available models from Fal.ai
        Uses a curated list of popular models as fallback
        """
        # Popular Fal.ai models - can be extended
        popular_models = [
            {
                "model_id": "fal-ai/flux/dev",
                "id": "fal-ai/flux/dev",  # Keep both for compatibility
                "name": "FLUX.1 [dev]",
                "category": ModelCategory.TEXT_TO_IMAGE,
                "description": "High-quality text-to-image generation model",
            },
            {
                "model_id": "fal-ai/flux/schnell",
                "id": "fal-ai/flux/schnell",
                "name": "FLUX.1 [schnell]",
                "category": ModelCategory.TEXT_TO_IMAGE,
                "description": "Fast text-to-image generation",
            },
            {
                "model_id": "fal-ai/fast-sdxl",
                "id": "fal-ai/fast-sdxl",
                "name": "Fast SDXL",
                "category": ModelCategory.TEXT_TO_IMAGE,
                "description": "Optimized SDXL for speed",
            },
            {
                "model_id": "fal-ai/stable-cascade",
                "id": "fal-ai/stable-cascade",
                "name": "Stable Cascade",
                "category": ModelCategory.TEXT_TO_IMAGE,
                "description": "High-fidelity image generation",
            },
        ]
        
        return popular_models

    def search_models(
        self,
        query: Optional[str] = None,
        category: Optional[ModelCategory] = None
    ) -> List[Dict[str, Any]]:
        """
        Search models in catalog

        Args:
            query: Search query string
            category: Filter by category

        Returns:
            List of matching models
        """
        all_models = self._get_all_models()
        results = []

        for model in all_models:
            # Category filter
            if category and model.get("category") != category:
                continue

            # Query filter
            if query:
                query_lower = query.lower()
                model_id = model.get("id") or model.get("model_id", "")
                searchable = f"{model_id} {model.get('name', '')} {model.get('description', '')}".lower()
                if query_lower not in searchable:
                    continue

            results.append(model)

        return results

    def get_model_info(self, model_id: str) -> Optional[Dict[str, Any]]:
        """Get detailed model information"""
        all_models = self._get_all_models()
        for model in all_models:
            if model.get("id") == model_id or model.get("model_id") == model_id:
                return model
        return None

    def list_categories(self) -> List[str]:
        """List available model categories"""
        return [cat.value for cat in ModelCategory]
