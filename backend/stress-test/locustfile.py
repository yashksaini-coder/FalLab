
from locust import task, between
from locust.contrib.fasthttp import FastHttpUser
import random

API_BASE = "/api/v1"
MODEL_IDS = [
    "fal-ai/flux/dev",
    "fal-ai/flux/schnell",
    "fal-ai/fast-sdxl",
    "fal-ai/flux-pro/v1.1-ultra",
    "fal-ai/flux-2/lora/edit",
]
PROMPTS = [
    "A serene mountain landscape at sunset",
    "Futuristic city with neon lights",
    "Abstract painting with vibrant colors",
    "Photorealistic portrait in studio lighting",
    "Peaceful forest path with sunlight",
]

MODEL_CATEGORIES = [
    "3d-to-3d",
    "audio-to-audio",
    "audio-to-video",
    "image-to-3d",
    "image-to-image",
    "image-to-json",
    "image-to-video",
    "json",
    "llm",
    "speech-to-speech",
    "speech-to-text",
    "text-to-3d",
    "text-to-audio",
    "text-to-image",
    "text-to-json",
    "text-to-speech",
    "text-to-video",
    "training",
    "video-to-audio",
    "video-to-video",
    "vision"
]
    

import time

MAX_PENDING_REQUESTS = 50


# ---
# To avoid global rate limiting during stress tests, each simulated user sends a unique X-User-ID header.
# The backend will use this header for per-user rate limiting if present.
# ---

class FalLabUser(FastHttpUser):
    wait_time = between(1, 2)
    request_ids = []
    SEARCH_QUERIES = [
        "flux", "diffusion", "anime", "photo", "art", "dev", "stable", "fast"
    ]
    CATEGORIES = [
        "art", "photo", "anime", "portrait", "landscape", "text-to-image", "image-to-image", "image-to-video", "inpainting"
    ]

    def on_start(self):
        # Assign a unique user ID for rate limiting
        self.user_id = f"locust-{id(self)}-{random.randint(1, 1000000)}"

    def _headers(self):
        return {"X-User-ID": self.user_id}

    # Example usage in a task:
    # with self.client.get(url, headers=self._headers(), ...) as response:

    def on_start(self):
        # Stagger cache refreshes across users (Fix 3)
        time.sleep(random.uniform(0, 5))
        # If you have a cache refresh method, call it here
        # self._refresh_models_cache()

    @task(2)
    def health_check(self):
        self.client.get(f"{API_BASE}/health", name="/health")

    @task(2)
    def list_models(self):
        self.client.get(f"{API_BASE}/models", name="/models")

    @task(2)
    def list_categories(self):
        self.client.get(f"{API_BASE}/models/categories", name="/models/categories")

    @task(2)
    def search_models(self):
        query = random.choice(self.SEARCH_QUERIES)
        params = {"q": query, "limit": 10}
        self.client.get(f"{API_BASE}/models/search", params=params, name="/models/search?q=*")

    @task(2)
    def filter_by_category(self):
        category = random.choice(self.CATEGORIES)
        params = {"category": category, "limit": 10}
        self.client.get(f"{API_BASE}/models", params=params, name="/models?category=*")

    # Removed invalid /models/categories/search task. Use only valid endpoints.

    @task(3)
    def submit_generation(self):
        payload = {
            "model_id": random.choice(MODEL_IDS),
            "prompt": random.choice(PROMPTS),
            "parameters": {"width": 1024, "height": 1024, "num_images": 1}
        }
        with self.client.post(f"{API_BASE}/generate", json=payload, catch_response=True, name="/generate") as response:
            if response.status_code == 200:
                try:
                    data = response.json()
                    req_id = data.get("request_id")
                    if req_id:
                        # Fix 1: Cap request storage and implement retirement
                        if len(self.request_ids) >= MAX_PENDING_REQUESTS:
                            self.request_ids.pop(0)
                        self.request_ids.append(req_id)
                        response.success()
                    else:
                        response.failure("No request_id in response")
                except Exception:
                    response.failure("Invalid JSON response")
            else:
                response.failure(f"Status {response.status_code}")

    @task(2)
    def check_status(self):
        if not self.request_ids:
            return
        # Fix 2: Add realistic delay before first status check
        time.sleep(random.uniform(3, 5))
        # Check only the LAST request (most recent)
        req_id = self.request_ids[-1]
        with self.client.get(f"{API_BASE}/status/{req_id}", catch_response=True, name="/status/{request_id}") as response:
            if response.status_code == 200:
                try:
                    data = response.json()
                    status = data.get("status")
                    # Fix 1: Retire completed/failed requests
                    if status in ["completed", "failed"]:
                        if req_id in self.request_ids:
                            self.request_ids.remove(req_id)
                    response.success()
                except Exception:
                    response.failure("Invalid JSON response")
            else:
                response.failure(f"Status {response.status_code}")
