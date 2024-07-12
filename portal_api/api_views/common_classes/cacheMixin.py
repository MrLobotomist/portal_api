from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page


class CacheMixin:
    cache_timeout = 30

    @method_decorator(cache_page(cache_timeout))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
