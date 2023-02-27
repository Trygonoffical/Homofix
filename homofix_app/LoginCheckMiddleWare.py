from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin


class LoginCheckMiddleWare(MiddlewareMixin):

    def process_view(self,request,view_func,view_args,view_kwargs):
        modulename=view_func.__module__
        print(modulename)
        user=request.user
        if user.is_authenticated:
            if user.user_type == "1":
                if modulename == "homofix_app.HodViews":
                    pass
                elif modulename == "homofix_app.views" or modulename == "django.views.static":
                    pass
                elif modulename == "django.contrib.auth.views" :
                    pass
                # else:
                #     return HttpResponseRedirect(reverse("admin_dashboard"))
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
            # elif user.user_type == "3":
            #     if modulename == "student_management_app.StudentViews" or modulename == "django.views.static":
            #         pass
            #     elif modulename == "student_management_app.views":
            #         pass
            #     else:
            #         return HttpResponseRedirect(reverse("student_home"))
            else:
                return HttpResponseRedirect(reverse("login"))

        else:
            if request.path == reverse("login") or request.path == reverse("login") or modulename == "django.contrib.auth.views"  or modulename=="homofix_app.views":
                pass
            else:
                return HttpResponseRedirect(reverse("login"))