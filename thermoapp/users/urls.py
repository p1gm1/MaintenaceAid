from django.urls import path

from thermoapp.users.views import (
    user_detail_view,
    user_redirect_view,
    user_update_view,
    LoginView,
    SignupView,
    LogoutView
)

app_name = "users"
urlpatterns = [
    path("~redirect/", view=user_redirect_view, name="redirect"),
    path("~update/", view=user_update_view, name="update"),
    path("<str:username>/", view=user_detail_view, name="detail"),
    path("login/", view=LoginView.as_view(), name="login"),
    path("signup/", view=SignupView.as_view(), name='signup'),
    path(route='logout/', view=LogoutView.as_view(), name='logout')
]
