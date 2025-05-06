# your_app/decorators.py
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.admin.views.decorators import staff_member_required

from django.views.decorators.http import require_http_methods, require_GET, require_POST
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views import View  # Import View for class-based views

from django.utils.decorators import method_decorator
from django.utils.decorators import decorator_from_middleware

from django.middleware.csrf import CsrfViewMiddleware
never_cache = decorator_from_middleware(CsrfViewMiddleware)


from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect






