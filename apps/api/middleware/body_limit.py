"""Bound request bodies before multipart parsing allocates upload files."""

import tempfile

from starlette.concurrency import run_in_threadpool
from starlette.responses import JSONResponse


MAX_REQUEST_BODY_BYTES = 16 * 1024 * 1024


class BodyLimitMiddleware:
    def __init__(self, app, max_body_bytes: int = MAX_REQUEST_BODY_BYTES):
        self.app = app
        self.max_body_bytes = max_body_bytes

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            return await self.app(scope, receive, send)
        lengths = [value for name, value in scope.get("headers", []) if name.lower() == b"content-length"]
        if lengths:
            if len(lengths) != 1 or not lengths[0].isdigit():
                return await JSONResponse({"detail": "Invalid Content-Length."}, status_code=400)(scope, receive, send)
            # Compare decimal bytes without converting an attacker-controlled
            # arbitrarily long integer (Python limits integer string parsing).
            declared = lengths[0].lstrip(b"0") or b"0"
            cap = str(self.max_body_bytes).encode("ascii")
            if len(declared) > len(cap) or (len(declared) == len(cap) and declared > cap):
                return await self._reject(scope, receive, send)

        # A bounded temporary spool avoids a second full in-memory request copy.
        # No downstream multipart parser sees data until the actual total is known.
        with tempfile.SpooledTemporaryFile(max_size=1024 * 1024) as body:
            total = 0
            while True:
                message = await receive()
                if message["type"] == "http.disconnect":
                    return
                chunk = message.get("body", b"")
                total += len(chunk)
                if total > self.max_body_bytes:
                    return await self._reject(scope, receive, send)
                await run_in_threadpool(body.write, chunk)
                if not message.get("more_body", False):
                    break
            await run_in_threadpool(body.seek, 0)
            remaining = total
            completed = False

            async def replay():
                nonlocal remaining, completed
                if completed:
                    return await receive()
                data = await run_in_threadpool(body.read, min(65536, remaining))
                remaining -= len(data)
                completed = remaining == 0
                return {"type": "http.request", "body": data, "more_body": not completed}

            await self.app(scope, replay, send)

    async def _reject(self, scope, receive, send):
        return await JSONResponse({"detail": "Request body exceeds the 16 MiB limit."}, status_code=413)(scope, receive, send)
