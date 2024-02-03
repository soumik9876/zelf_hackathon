import logging
from .models import Constant
from .constants import ConstantKeyValue

def get_logger(name='django'):
    return logging.getLogger(name)


def get_request_str(request):
    meta = request.META
    return f"{request.method} {request.get_full_path()} {meta.get('SERVER_PROTOCOL')} {meta.get('HTTP_USER_AGENT')}"


def get_debug_str(request, user, errors):
    return (
        f"""
        request: {get_request_str(request)}
        user: {f"{user} ({user.id})" if user else ""}
        data: {request.data}
        errors: {errors}"""
    )

def get_constant(constant):
    key, value = constant
    try:
        constant = Constant.objects.get(key=key)
    except Constant.DoesNotExist:
        constant = Constant.objects.create(key=key, value=value)
    return constant.value