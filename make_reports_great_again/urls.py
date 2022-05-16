from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include, re_path
from django.views.static import serve

from django.contrib.auth import views as auth_views

from core.views import markdown_uploader
from make_reports_great_again import settings


admin.site.site_header = 'Make Reports Great Again - Admin Panel'                    # default: "Django Administration"
admin.site.index_title = 'Write awesome reports'                 # default: "Site administration"
admin.site.site_title = 'Make Report Great Agains - Admin Panel' # default: "Django site admin"
urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^chaining/', include('smart_selects.urls')),
    re_path('', include("core.urls"), name="core"),
    path('martor/', include('martor.urls')),
    path('accounts/login/', auth_views.LoginView.as_view()),
    re_path(r'^api/uploader/$', markdown_uploader, name='markdown_uploader_page'),

]

urlpatterns = [
                  re_path(r'^media/(?P<path>.*)$', serve,
                      {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
              ] + staticfiles_urlpatterns() + urlpatterns
