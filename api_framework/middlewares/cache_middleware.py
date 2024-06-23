from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp
from typing import Callable
from diskcache import Cache
import hashlib

class CacheMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp, ttl: int = 1800):
        super().__init__(app)
        self.cache = Cache(directory="cache_directory")
        self.ttl = ttl

    async def dispatch(self, request: Request, call_next: Callable):
        # Create a cache key based on the request URL
        cache_key = hashlib.md5(str(request.url).encode()).hexdigest()

        print("Hello")
        # Check for cache
        cached_response = self.cache.get(cache_key)
        if cached_response:
            return Response(content=cached_response, headers={"x-cache": "True"})
        
        # No Cache, process the request
        response = await call_next(request)
        response.headers["x-cache"] = "False"

        # Cache Successfull Responses
        if response.status_code == 200:
            self.cache.set(cache_key, response.body(), expire=self.ttl)

        return response
