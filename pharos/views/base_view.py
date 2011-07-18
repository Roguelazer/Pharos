import os.path

import pystache

class BaseView(pystache.View):
    template_path = os.path.dirname(__file__)
