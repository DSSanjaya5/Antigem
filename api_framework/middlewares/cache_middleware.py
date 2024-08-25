import json
from fastapi import Request
from fastapi.responses import JSONResponse
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
        # Add the endpoints that are to be cached to the api_paths
        api_paths = ["/hello_world", "/endpoint"]
        if request.url.path not in api_paths:
            return await call_next(request)

        # Create a cache key based on the request URL
        cache_key = hashlib.md5(str(request.url).encode()).hexdigest()

        # Check for cache
        cached_response = self.cache.get(cache_key)
        if cached_response:
            return JSONResponse(
                content=json.loads(cached_response),
                headers={"x-cache": "True"},
                status_code=200,
            )

        # No Cache, process the request
        response = await call_next(request)

        # Cache Successfull Responses
        if response.status_code == 200:
            body = []
            async for chunk in response.body_iterator:
                body.append(chunk.decode("utf-8"))
            body = "".join(body)
            self.cache.set(cache_key, body, expire=self.ttl)

        return JSONResponse(
            content=json.loads(body), headers={"x-cache": "False"}, status_code=200
        )
