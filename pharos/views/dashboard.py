import datetime

from .base_view import BaseView

class Dashboard(BaseView):
    def generated_when(self):
        return datetime.datetime.now().strftime("%X %x")
