# -*- coding: UTF-8 -*-


def _wraper(fn):
    def _render(*args, **kwagrs):
        request = args[0]
        http_content = args[2]
        page = request.GET.get('dt_page', 0)
        try:
            page = int(page)
        except:
            page = 0
        http_content.update({'dt_page': page})
        return fn(*args, **kwagrs)
    return _render
__import__("django.shortcuts")
sys = __import__("sys")
_render_module = sys.modules['django.shortcuts']
_render_module.render = _wraper(_render_module.render)

