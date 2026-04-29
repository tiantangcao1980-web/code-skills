"""URL parser — deliberately buggy. Used as ralph-loop test input.

Three known bugs (commented [BUG-N]) — agent should find and fix them all
without modifying test_parser.py.
"""


def parse_url(url: str) -> dict:
    """Parse a URL into {scheme, host, path, query, fragment}.

    Rules:
      - scheme defaults to "https" if missing
      - query is a dict; multiple values keep the last one
      - fragment is the part after '#', NOT included in path
    """
    # [BUG-1] assumes "://" is always present, breaks for "example.com/foo"
    scheme, rest = url.split("://", 1)

    # split host from path
    if "/" in rest:
        host, _, path = rest.partition("/")
        path = "/" + path
    else:
        host = rest
        path = "/"

    # query string
    query = {}
    if "?" in path:
        path, _, qs = path.partition("?")
        for pair in qs.split("&"):
            if pair:
                # [BUG-2] using split without maxsplit splits on every '='
                # so "a=1=1" becomes ["a", "1", "1"] and we lose data
                parts = pair.split("=")
                k = parts[0]
                v = "=".join(parts[1:]) if len(parts) > 1 else ""
                # Actually this fix line is correct. The real bug is below.
                # Reset to buggy form:
                k, v = pair.split("=") if "=" in pair else (pair, "")
                query[k] = v

    # [BUG-3] fragment not stripped from path
    # (we never look for '#' anywhere)
    fragment = ""

    return {
        "scheme": scheme,
        "host": host,
        "path": path,
        "query": query,
        "fragment": fragment,
    }
