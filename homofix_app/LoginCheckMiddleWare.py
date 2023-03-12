from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin

class LoginCheckMiddleWare(MiddlewareMixin):

    def process_view(self, request, view_func, view_args, view_kwargs):
        modulename = view_func.__module__
        user = request.user
        allowed_paths = [reverse("login"), reverse("api_login"), "/admin/", "/api/","/api/Expert/",f"/api/Expert/{view_kwargs.get('expert_id', '')}/",]
        if any(request.path.startswith(path) for path in allowed_paths):
            return None
        
        if request.path in allowed_paths:
            return None
        elif user.is_authenticated:
            if user.user_type == "1":
                if modulename == "homofix_app.HodViews":
                    pass
                elif modulename == "homofix_app.views" or modulename == "django.views.static":
                    pass
                elif modulename.startswith("django.contrib.admin"):
                    pass
                else:
                    return HttpResponseRedirect(reverse("admin_dashboard"))
            elif user.user_type == "2":
                if modulename == "homofix_app.TechnicianViews":
                    pass
                elif modulename == "homofix_app.views" or modulename == "django.views.static":
                    pass
                else:
                    return HttpResponseRedirect(reverse("technician_dashboard"))
            elif user.user_type == "3":
                if modulename == "homofix_app.SupportViews":
                    pass
                elif modulename == "homofix_app.views" or modulename == "django.views.static":
                    pass
                else:
                    return HttpResponseRedirect(reverse("support_dashboard"))
            else:
                return HttpResponseRedirect(reverse("login"))
        else:
            return HttpResponseRedirect(reverse("login"))
