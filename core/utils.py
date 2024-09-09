def derive_canonical_url(request):
    scheme = request.scheme
    host = request.get_host()
    if not host.startswith('www.'):
        host = f'www.{host}'
    path = request.path
    return f'{scheme}://{host}{path}'


def derive_absolute_url(request):
    scheme = request.scheme
    host = request.get_host()
    if not host.startswith('www.'):
        host = f'www.{host}'
    full_path = request.get_full_path()
    return f'{scheme}://{host}{full_path}'


def hreflang_and_x_default_link(canonical_url):
    return (
        f'<link rel="alternate" hreflang="en" href="{canonical_url}" />'
        f'\n<link rel="alternate" hreflang="x-default" href="{canonical_url}" />'
    )
