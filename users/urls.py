from django.urls import path
from users.views import (
    register,
    login,
    logout,
    profile,
    profile_info,

    add_chat,
    chat,
    start_private,
    chat_info,
    add_member,
    change_member_status,

    add_friend,

    home,
)

app_name = "users"

urlpatterns = [
    path("register/", register, name="register"),
    path("login/", login, name="login"),
    path("logout/", logout, name="logout"),
    path("profile/", profile, name="profile"),
    path("profile/<str:username>", profile, name="profile"),
    path("profile-info/", profile_info, name="profile-info"),

    path("add-chat/", add_chat, name="add-chat"),
    path("chat/<int:id>/", chat, name="chat"),
    path("start-private/<int:id>/", start_private, name="start-private"),
    path("chat-info/<int:id>/", chat_info, name="chat-info"),
    path("chat-info/change/<int:id>/", chat_info, name="chat-info_change"),
    path("add-member/<int:group_id>/", add_member, name="add-member"),
    path("change-member-status/<int:group_id>/<int:user_id>/", change_member_status, name="change-member-status"),

    path("add-friend/", add_friend, name="add-friend"),
    
    path("", home, name="home"),
]
