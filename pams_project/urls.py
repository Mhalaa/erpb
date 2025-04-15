from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView
from django.views.generic import RedirectView

class CustomLoginView(LoginView):
    template_name = 'pams/login.html'  # We’ll create this later
    def get_success_url(self):
        user_profile = self.request.user.profile
        if user_profile.role == 'admin':
            return '/admin/'
        elif user_profile.role == 'md':
            return '/md-approvals/'
        elif user_profile.role == 'ceo':
            return '/ceo-approvals/'
        elif user_profile.role == 'finance':
            return '/finance-approvals/'
        else:
            return '/dashboard/'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', CustomLoginView.as_view(), name='login'),
    path('dashboard/', RedirectView.as_view(url='/index/'), name='dashboard'),  # Placeholder
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])