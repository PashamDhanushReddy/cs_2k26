from django.http import JsonResponse
from django.shortcuts import render

def custom_csrf_failure(request, reason=""):
    """Custom CSRF failure view to provide better error messages"""
    if request.method == 'POST':
        return JsonResponse({
            'error': 'CSRF verification failed',
            'reason': reason,
            'solution': 'Please refresh the page and try again. Make sure cookies are enabled in your browser.',
            'debug_info': {
                'method': request.method,
                'origin': request.META.get('HTTP_ORIGIN', 'Not set'),
                'referer': request.META.get('HTTP_REFERER', 'Not set'),
                'content_type': request.META.get('CONTENT_TYPE', 'Not set'),
            }
        }, status=403)
    else:
        return render(request, 'website/csrf_error.html', {
            'reason': reason,
            'debug_info': {
                'method': request.method,
                'origin': request.META.get('HTTP_ORIGIN', 'Not set'),
                'referer': request.META.get('HTTP_REFERER', 'Not set'),
                'content_type': request.META.get('CONTENT_TYPE', 'Not set'),
            }
        })