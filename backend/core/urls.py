from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.contrib.sitemaps.views import sitemap
from django.views.generic.base import TemplateView

from account.forms import StylesCustomPasswordResetForm, StylesCustomSetPasswordForm
from main.sitemap import StaticViewSitemap, HomeViewSitemap, CategoryViewSitemap

sitemaps = {
    'home': HomeViewSitemap,
    'categories': CategoryViewSitemap,
    'static': StaticViewSitemap,
}

urlpatterns = ([

    path('admin/', admin.site.urls),
    path('api/', include('api.urls', namespace='api')),
    path('', include('main.urls', namespace='main')),
    path('', include('account.urls', namespace='account')),
    path('', include('campaign.urls', namespace='campaign')),
    path('', include('cms.urls', namespace='cms')),
    path('checkout/', include('checkout.urls', namespace='checkout')),
    path(
        "reset_password/",
        auth_views.PasswordResetView.as_view(
            template_name="password_reset.html",
            form_class=StylesCustomPasswordResetForm, ),
        name="reset_password"
    ),
    path(
        "reset_password_done/",
        auth_views.PasswordResetDoneView.as_view(template_name="password_reset_done.html"),
        name="password_reset_done"
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="password_reset_form.html",
            form_class=StylesCustomSetPasswordForm
        ),
        name="password_reset_confirm"
    ),
    path(
        "reset_password_complete/",
        auth_views.PasswordResetCompleteView.as_view(template_name="password_reset_complete.html"),
        name="password_reset_complete"
    ),
    path("ckeditor5/", include('django_ckeditor_5.urls')),
    path('sitemap.xml/', sitemap, {'sitemaps': sitemaps}),
    path(
        "robots.txt/",
        TemplateView.as_view(template_name="robots.txt", content_type="text/plain"), )
])
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
