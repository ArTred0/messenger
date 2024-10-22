from django.urls import path
from users.views import (
    register,
    login,
    logout,
    profile,
    add_chat,
    chat,
    delete_message,
    reject_friend,
    delete_friend,
    search_user,
    add_friend,
    home,
    accept_friend,
    delete_friend,
    cancel_request,
)

app_name = "users"

urlpatterns = [
    path("register/", register, name="register"),
    path("login/", login, name="login"),
    path("logout/", logout, name="logout"),
    path("profile/", profile, name="profile"),
    path("profile/<str:username>", profile, name="profile"),
    path("add_chat/", add_chat, name="add_chat"),
    path("chat/<int:id>", chat, name="chat"),
    path("delete_message/<int:id>", delete_message, name="delete_message"),
    path("search_user/<str:username>", search_user, name="search_user"),
    path("add_friend/", add_friend, name="add_friend"),
    path("accept_friend/<int:id>", accept_friend, name="accept_friend"),
    path("reject_friend/<int:id>", reject_friend, name="reject_friend"),
    path("reject_friend/<int:id>", reject_friend, name="reject_friend"),
    path("delete_friend/<int:id>", delete_friend, name="delete_friend"),
    path("cancel_request/<int:id>", cancel_request, name="cancel_request"),
    path("", home, name="home"),
]
