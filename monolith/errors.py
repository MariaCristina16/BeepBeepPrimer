from flask import make_response, render_template
from monolith.views.home import index


def render_error_page(e):  # pragma: no cover
    """
    This function is a callback and it is called when an HTTPExcpetion is thrown
    We will decide in future how to manage different errors
    """
    if e.code == 401 or e.code == 403:
        return make_response(index(), e.code)
    elif e.code == 404:
        return make_response(render_template('not_found.html', exception=e), e.code)
