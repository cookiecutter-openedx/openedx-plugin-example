from collections import Set
from django.http import HttpResponse
from django.utils.translation import get_language_bidi
from django.views import View
from openedx.core.djangoapps.plugin_api.views import EdxFragmentView
from web_fragments.fragment import Fragment


def api_panel(request):
    return HttpResponse("result")


class ApiView(View):
    def get(self, request):
        # <view logic>
        return HttpResponse("result")

    def render_to_fragment(self, request):
        # <view logic>
        return HttpResponse("result@@@")


class EdxApiFragmentView(EdxFragmentView):
    """
    Component implementation of the discussion board.
    """

    def render_to_fragment(self, request, course_id=None, discussion_id=None, thread_id=None, **kwargs):
        """
        Render the discussion board to a fragment.
        Args:
            request: The Django request.
            course_id: The id of the course in question.
            discussion_id: An optional discussion ID to be focused upon.
            thread_id: An optional ID of the thread to be shown.
        Returns:
            Fragment: The fragment representing the discussion board
        """
        return Fragment("HELLO")

    def vendor_js_dependencies(self):
        """
        Returns list of vendor JS files that this view depends on.
        The helper function that it uses to obtain the list of vendor JS files
        works in conjunction with the Django pipeline to ensure that in development mode
        the files are loaded individually, but in production just the single bundle is loaded.
        """
        dependencies = Set()
        dependencies.update(self.get_js_dependencies("discussion_vendor"))
        return list(dependencies)

    def js_dependencies(self):
        """
        Returns list of JS files that this view depends on.
        The helper function that it uses to obtain the list of JS files
        works in conjunction with the Django pipeline to ensure that in development mode
        the files are loaded individually, but in production just the single bundle is loaded.
        """
        return self.get_js_dependencies("discussion")

    def css_dependencies(self):
        """
        Returns list of CSS files that this view depends on.
        The helper function that it uses to obtain the list of CSS files
        works in conjunction with the Django pipeline to ensure that in development mode
        the files are loaded individually, but in production just the single bundle is loaded.
        """
        if get_language_bidi():
            return self.get_css_dependencies("style-discussion-main-rtl")
        else:
            return self.get_css_dependencies("style-discussion-main")
