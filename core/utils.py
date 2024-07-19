def derive_canonical_url(request):
    scheme = request.scheme
    host = request.get_host()
    if not host.startswith('www.'):
        host = f'www.{host}'
    path = request.path
    return f'{scheme}://{host}{path}'
