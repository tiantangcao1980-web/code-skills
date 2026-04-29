"""URL parser — fixed version. All 3 bugs from before/parser.py addressed."""


def parse_url(url: str) -> dict:
    """Parse a URL into {scheme, host, path, query, fragment}."""
    # [FIX-1] handle missing scheme
    if "://" in url:
        scheme, rest = url.split("://", 1)
    else:
        scheme, rest = "https", url

    # [FIX-3] strip fragment first so it doesn't leak into path/query
    if "#" in rest:
        rest, fragment = rest.split("#", 1)
    else:
        fragment = ""

    if "/" in rest:
        host, _, path = rest.partition("/")
        path = "/" + path
    else:
        host = rest
        path = "/"

    query = {}
    if "?" in path:
        path, _, qs = path.partition("?")
        for pair in qs.split("&"):
            if not pair:
                continue
            # [FIX-2] split with maxsplit=1 so values can contain '='
            k, _, v = pair.partition("=")
            query[k] = v

    return {
        "scheme": scheme,
        "host": host,
        "path": path,
        "query": query,
        "fragment": fragment,
    }
