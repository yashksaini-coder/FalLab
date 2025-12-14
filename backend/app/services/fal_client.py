import aiohttp
import logging
import asyncio
from typing import Optional, Dict, Any, List
from datetime import datetime

logger = logging.getLogger(__name__)


class FalAIClient:
    """
    Professional Fal.ai client for interacting with:
    - Fal.ai Platform APIs (https://api.fal.ai/v1) - Model discovery
    - Queue API (https://queue.fal.run) - Async generation
    - Sync API (https://fal.run) - Blocking generation
    """

    PLATFORM_API_URL = "https://api.fal.ai/v1"
    QUEUE_API_URL = "https://queue.fal.run"
    SYNC_API_URL = "https://fal.run"

    def __init__(self, api_key: str):
        """
        Initialize Fal.ai client

        Args:
            api_key: Fal.ai API key for authentication
        """
        self.api_key = api_key
        self.headers = {
            "Authorization": f"Key {api_key}",
            "Content-Type": "application/json"
        }

    async def _get_models_list(self) -> List[Dict[str, Any]]:
        """
        Fetch complete list of available models from Fal.ai Platform API
        Handles pagination automatically

        API Endpoint: GET https://api.fal.ai/v1/models

        Expected Response Structure:
        {
            "models": [
                {
                    "endpoint_id": "fal-ai/flux/dev",
                    "metadata": {
                        "display_name": "FLUX.1 [dev]",
                        "category": "text-to-image",
                        "description": "...",
                        "status": "active",
                        "tags": ["fast", "high-quality"],
                        "thumbnail_url": "...",
                        "model_url": "https://fal.run/fal-ai/flux/dev",
                        ...
                    }
                },
                ...
            ],
            "total": 150,
            "next_cursor": "..." (optional)
        }

        Returns:
            List of model dictionaries with endpoint_id and metadata

        Raises:
            Exception: If API request fails
        """
        try:
            models = []
            cursor = None
            total_fetched = 0

            async with aiohttp.ClientSession() as session:
                while True:
                    url = f"{self.PLATFORM_API_URL}/models"
                    params = {"cursor": cursor} if cursor else {}

                    logger.debug(f"Fetching models from {url}" + (f" with cursor={cursor}" if cursor else ""))

                    async with session.get(
                        url,
                        headers=self.headers,
                        params=params,
                        timeout=aiohttp.ClientTimeout(total=30)
                    ) as response:
                        if response.status != 200:
                            error_text = await response.text()
                            logger.error(f"Fal.ai API error {response.status}: {error_text}")
                            raise Exception(f"Failed to fetch models: HTTP {response.status}")

                        data = await response.json()

                        # Extract models from response
                        batch = data.get('models', [])
                        models.extend(batch)
                        total_fetched += len(batch)
                        logger.info(f"Fetched {len(batch)} models (total so far: {total_fetched})")

                        # Check for pagination
                        cursor = data.get('next_cursor')
                        if not cursor:
                            logger.info(f"Successfully fetched all {len(models)} models from Fal.ai")
                            break

            return models

        except Exception as e:
            logger.error(f"Error fetching models from Fal.ai: {str(e)}", exc_info=True)
            raise

    def search_models(
        self,
        query: str,
        models: List[Dict[str, Any]],
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Perform client-side search on cached models list.
        Since Fal.ai doesn't provide a dedicated search API, we search locally.

        Searches in:
        - endpoint_id (highest priority)
        - metadata.display_name
        - metadata.description
        - metadata.tags

        Args:
            query: Search query string
            models: List of models to search in
            limit: Maximum number of results to return

        Returns:
            List of matching models sorted by relevance
        """
        if not query or not query.strip():
            return models[:limit]

        query_lower = query.lower()
        results = []

        for model in models:
            score = 0

            # Priority 1: endpoint_id match (exact or partial)
            endpoint_id = model.get('endpoint_id', '').lower()
            if query_lower in endpoint_id:
                score += 5
                if endpoint_id == query_lower:  # Exact match bonus
                    score += 10

            metadata = model.get('metadata', {})

            # Priority 2: display_name match
            display_name = metadata.get('display_name', '').lower()
            if query_lower in display_name:
                score += 3
                if display_name == query_lower:  # Exact match bonus
                    score += 5

            # Priority 3: description match
            description = metadata.get('description', '').lower()
            if query_lower in description:
                score += 1

            # Priority 3: tag match
            tags = metadata.get('tags', [])
            if any(query_lower in tag.lower() for tag in tags):
                score += 2

            if score > 0:
                results.append((model, score))

        # Sort by score (highest first) and extract models
        results.sort(key=lambda x: x[1], reverse=True)
        sorted_results = [m for m, _ in results[:limit]]

        logger.debug(f"Search for '{query}' found {len(sorted_results)} results")
        return sorted_results

    def get_models_by_category(
        self,
        models: List[Dict[str, Any]],
        category: str
    ) -> List[Dict[str, Any]]:
        """
        Filter models by category

        Args:
            models: List of models to filter
            category: Category to filter by (e.g., 'text-to-image')

        Returns:
            List of models in the specified category
        """
        category_lower = category.lower()
        filtered = [
            m for m in models
            if m.get('metadata', {}).get('category', '').lower() == category_lower
        ]
        logger.debug(f"Found {len(filtered)} models in category '{category}'")
        return filtered

    def get_model_info(
        self,
        endpoint_id: str,
        models: List[Dict[str, Any]]
    ) -> Optional[Dict[str, Any]]:
        """
        Get detailed information for a specific model

        Args:
            endpoint_id: Model endpoint ID (e.g., 'fal-ai/flux/dev')
            models: List of models to search in

        Returns:
            Model information dict or None if not found
        """
        for model in models:
            if model.get('endpoint_id') == endpoint_id:
                logger.debug(f"Found model info for: {endpoint_id}")
                return model
        logger.warning(f"Model not found: {endpoint_id}")
        return None

    def get_active_models(self, models: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Filter to only active models

        Args:
            models: List of models to filter

        Returns:
            List of active models only
        """
        active = [
            m for m in models
            if m.get('metadata', {}).get('status') == 'active'
        ]
        logger.debug(f"Filtered {len(active)} active models from {len(models)} total")
        return active

    def get_categories(self, models: List[Dict[str, Any]]) -> List[str]:
        """
        Get list of unique categories from models

        Args:
            models: List of models

        Returns:
            Sorted list of unique category names
        """
        categories = set()
        for model in models:
            category = model.get('metadata', {}).get('category')
            if category:
                categories.add(category)
        result = sorted(list(categories))
        logger.debug(f"Found {len(result)} unique categories")
        return result

    async def submit_request(
        self,
        model_id: str,
        input_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Submit a generation request to Fal.ai Queue API (async)

        API Endpoint: POST https://queue.fal.run/<model_id>

        Request format:
        {
            "prompt": "A serene mountain landscape",
            "width": 1024,
            "height": 1024,
            ...
        }

        Response format:
        {
            "request_id": "req_abc123...",
            "status": "queued",
            "queue_position": 5
        }

        Args:
            model_id: Model endpoint ID
            input_data: Input parameters for the model

        Returns:
            Response containing request_id and status

        Raises:
            Exception: If request submission fails
        """
        try:
            async with aiohttp.ClientSession() as session:
                url = f"{self.QUEUE_API_URL}/{model_id}"

                logger.info(f"Submitting async request to {model_id}")

                async with session.post(
                    url,
                    json=input_data,
                    headers=self.headers,
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    if response.status not in (200, 201):
                        error_text = await response.text()
                        logger.error(f"Queue API error {response.status}: {error_text}")
                        raise Exception(f"Failed to submit request: HTTP {response.status}")

                    result = await response.json()
                    request_id = result.get('request_id')
                    logger.info(f"Request submitted for {model_id}: {request_id}")
                    return result

        except Exception as e:
            logger.error(f"Error submitting request to {model_id}: {str(e)}", exc_info=True)
            raise

    async def get_request_status(self, request_id: str) -> Dict[str, Any]:
        """
        Get status of a queued generation request

        API Endpoint: GET https://queue.fal.run/requests/<request_id>

        Response format:
        {
            "request_id": "req_abc123...",
            "status": "processing" | "completed" | "failed",
            "queue_position": 2,
            "result": {...},  # Only if completed
            "error": "..."    # Only if failed
        }

        Args:
            request_id: Request ID from submit_request

        Returns:
            Status information including current status and result

        Raises:
            Exception: If status check fails
        """
        try:
            async with aiohttp.ClientSession() as session:
                url = f"{self.QUEUE_API_URL}/requests/{request_id}"

                async with session.get(
                    url,
                    headers=self.headers,
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        logger.error(f"Status API error {response.status}: {error_text}")
                        raise Exception(f"Failed to get status: HTTP {response.status}")

                    return await response.json()

        except Exception as e:
            logger.error(f"Error getting status for request {request_id}: {str(e)}", exc_info=True)
            raise

    async def generate_sync(
        self,
        model_id: str,
        input_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Perform synchronous (blocking) generation.
        Waits for the generation to complete before returning.

        API Endpoint: POST https://fal.run/<model_id>

        This is a simpler endpoint that blocks until completion.
        Use for smaller models or when you need the result immediately.

        Args:
            model_id: Model endpoint ID
            input_data: Input parameters for the model

        Returns:
            Generation result

        Raises:
            Exception: If generation fails or times out
        """
        try:
            async with aiohttp.ClientSession() as session:
                url = f"{self.SYNC_API_URL}/{model_id}"

                logger.info(f"Submitting sync request to {model_id}")

                async with session.post(
                    url,
                    json=input_data,
                    headers=self.headers,
                    timeout=aiohttp.ClientTimeout(total=300)  # 5 minute timeout
                ) as response:
                    if response.status not in (200, 201):
                        error_text = await response.text()
                        logger.error(f"Sync API error {response.status}: {error_text}")
                        raise Exception(f"Generation failed: HTTP {response.status}")

                    result = await response.json()
                    logger.info(f"Sync generation completed for {model_id}")
                    return result

        except asyncio.TimeoutError:
            logger.error(f"Sync generation timeout for {model_id}")
            raise Exception("Generation timeout - request took too long (5 minutes)")
        except Exception as e:
            logger.error(f"Error during sync generation with {model_id}: {str(e)}", exc_info=True)
            raise

    async def poll_request(
        self,
        request_id: str,
        max_attempts: int = 120,
        poll_interval: int = 1
    ) -> Dict[str, Any]:
        """
        Poll a request until completion.

        Repeatedly checks request status until:
        - status == "completed" → Returns result
        - status == "failed" → Raises exception
        - Timeout exceeded → Raises exception

        Args:
            request_id: Request ID to poll
            max_attempts: Maximum number of poll attempts
            poll_interval: Seconds between polls (default: 1 second)

        Returns:
            Final result when completed

        Raises:
            Exception: If request fails or times out
        """
        attempts = 0

        while attempts < max_attempts:
            try:
                status_response = await self.get_request_status(request_id)
                current_status = status_response.get('status')

                logger.debug(
                    f"Poll {request_id}: status={current_status} "
                    f"(attempt {attempts + 1}/{max_attempts})"
                )

                if current_status == 'completed':
                    logger.info(f"Request {request_id} completed successfully")
                    return status_response

                elif current_status == 'failed':
                    error_msg = status_response.get('error', 'Unknown error')
                    logger.error(f"Request {request_id} failed: {error_msg}")
                    raise Exception(f"Generation failed: {error_msg}")

                # Still processing, wait before next poll
                attempts += 1
                if attempts < max_attempts:
                    await asyncio.sleep(poll_interval)

            except Exception as e:
                if "Generation failed" in str(e):
                    raise  # Re-raise generation failures
                logger.error(f"Error polling request {request_id}: {str(e)}")
                raise

        logger.error(f"Request {request_id} timeout after {max_attempts * poll_interval} seconds")
        raise Exception(
            f"Request timeout - generation did not complete within "
            f"{max_attempts * poll_interval} seconds"
        )
