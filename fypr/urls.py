from django.contrib import admin
from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static
from .settings import MEDIA_ROOT,MEDIA_URL

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
#    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [

    # path('swagger/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('api/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('doc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    path('admin/', admin.site.urls),
    path('signup/', views.signup),
    path('login/', views.login),
    path('profile-update/', views.profile_update),


    path('send-verification-link-again/', views.send_verification_link_again),
    path('email-confirmation/<uuid>', views.email_confirmation),

    path('allprojects/', views.all_projects),
    path('allreviews/<int:pk>', views.all_reviews),

    path('projects/<int:pk>', views.projects_by_category),
    path('category/', views.category),

    path('userprojects/', views.get_projects),
    path('create-project/', views.create_project),
    path('update-project/<int:pk>', views.update_project),
    path('delete-project/<int:pk>', views.delete_project),

    path('project-images/<int:pk>', views.delete_project),

    path('project-reviews/<int:pid>', views.get_reviews),
    path('create-review/<int:pid>', views.create_review),
    path('update-review/<int:rid>', views.update_review),
    path('delete-review/<int:rid>', views.delete_review),




]
urlpatterns += static(MEDIA_URL,document_root=MEDIA_ROOT)
# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)