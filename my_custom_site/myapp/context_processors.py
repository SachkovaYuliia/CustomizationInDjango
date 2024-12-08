from datetime import  datetime

def global_context(request):
    """
       Контекстний процесор для передачі глобальних даних.
    """
    return {
        'current_year': datetime.now().year,
        'global_message': 'Welcome to our site!',
    }