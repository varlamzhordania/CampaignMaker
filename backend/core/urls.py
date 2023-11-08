"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from account.forms import StylesCustomPasswordResetForm, StylesCustomSetPasswordForm
from django.contrib.sitemaps.views import sitemap
from main.sitemap import StaticViewSitemap, HomeViewSitemap, CategoryViewSitemap
from django.views.generic.base import TemplateView



sitemaps = {
    'home': HomeViewSitemap,
    'categories': CategoryViewSitemap,
    'static': StaticViewSitemap,
}

urlpatterns = [

                  path('admin/', admin.site.urls),
                  path('', include('main.urls', namespace='main')),
                  path('', include('account.urls', namespace='account')),
                  path('', include('campaign.urls', namespace='campaign')),
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
                  path("robots.txt/",TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),)
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) \
              + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
