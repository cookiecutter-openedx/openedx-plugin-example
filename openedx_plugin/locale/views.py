import logging
from urllib.parse import urljoin

from django.shortcuts import redirect

from .utils import get_marketing_site

log = logging.getLogger(__name__)


def marketing_redirector(request):
    """
    Receives urls from MKTG_URL_OVERRIDES such as

    MKTG_URL_OVERRIDES: {
        "COURSES": "https://lms.example.edu/marketing-redirector?example_page=learning-content",
    }

    analyzes the request object to determine the best marketing site to redirect to.
    example: example.org/learning-content

    """
    url = get_marketing_site(request)
    example_page = request.GET.get("example_page") or ""
    redirect_to = urljoin(url, example_page)

    return redirect(redirect_to)
