"""
Nirikshak API Security Headers Middleware.
Enforces defense-in-depth HTTP response headers for all API traffic.
"""

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """
    Injects enterprise-grade HTTP security headers into every outbound response.
    Protects against clickjacking, MIME-sniffing, XSS, and unauthorized framing.
    """

    SECURE_HEADERS = {
        "X-Content-Type-Options": "nosniff",
        "X-Frame-Options": "DENY",
        "X-XSS-Protection": "1; mode=block",
        "Referrer-Policy": "strict-origin-when-cross-origin",
        "Permissions-Policy": "camera=(), microphone=(), geolocation=(), payment=()",
        "Content-Security-Policy": (
            "default-src 'self'; "
            "img-src 'self' data: blob:; "
            "script-src 'self'; "
            "style-src 'self' 'unsafe-inline'; "
            "frame-ancestors 'none'; "
            "object-src 'none'; "
            "base-uri 'self';"
        ),
        "Strict-Transport-Security": "max-age=31536000; includeSubDomains; preload",
    }

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        response = await call_next(request)
        for header, value in self.SECURE_HEADERS.items():
            response.headers[header] = value
        return response
