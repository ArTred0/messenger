from django.urls import path
from users.views import (
    register,
    login,
    logout,
    profile,
    profile_info,

    add_chat,
    chat,
    delete_message,
    search_chat,
    start_private,
    enter_chat,
    chat_info,
    add_member,
    remove_member,
    change_member_status,
    delete_group,
    leave_group,

    search_user,
    add_friend,
    reject_friend,
    accept_friend,
    delete_friend,
    cancel_request,

    toggle_theme,

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
    path("delete-message/<int:id>/", delete_message, name="delete-message"),
    path("search-chat/<str:name>/", search_chat, name="search-chat"),
    path("enter-chat/<int:id>/", enter_chat, name="enter-chat"),
    path("start-private/<int:id>/", start_private, name="start-private"),
    path("chat-info/<int:id>/", chat_info, name="chat-info"),
    path("chat-info/change/<int:id>/", chat_info, name="chat-info_change"),
    path("add-member/<int:group_id>/", add_member, name="add-member"),
    path("change-member-status/<int:group_id>/<int:user_id>/", change_member_status, name="change-member-status"),
    path("remove-member/<int:group_id>/<int:user_id>/", remove_member, name="remove-member"),
    path("delete-group/<int:id>/", delete_group, name="delete-group"),
    path("leave-group/<int:id>/", leave_group, name="leave-group"),

    path("search-user/<str:username>/", search_user, name="search-user"),
    path("add-friend/", add_friend, name="add-friend"),
    path("accept-friend/<int:id>/", accept_friend, name="accept-friend"),
    path("reject-friend/<int:id>/", reject_friend, name="reject-friend"),
    path("delete-friend/<int:id>/", delete_friend, name="delete-friend"),
    path("cancel-request/<int:id>/", cancel_request, name="cancel-request"),
    
    path("toggle-theme/<str:state>/", toggle_theme, name="toggle-theme"),

    path("", home, name="home"),
]
