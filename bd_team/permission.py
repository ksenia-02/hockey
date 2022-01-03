from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import Http404
from django.shortcuts import redirect


class MyPermissionMixin(PermissionRequiredMixin):

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return redirect('error_access')
        return super().dispatch(request, *args, **kwargs)