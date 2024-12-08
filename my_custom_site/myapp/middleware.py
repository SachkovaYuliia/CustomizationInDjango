import logging

logger = logging.getLogger('myapp')

class RequestCountMiddleware:
    request_count = 0

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        RequestCountMiddleware.request_count += 1
        logger.info(f"Request #{RequestCountMiddleware.request_count} to {request.path}")
        response = self.get_response(request)
        return response