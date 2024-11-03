from django.urls import path
from api.views import (
    check_new_messages,
    send_message,
    delete_message,
    change_message,
    search_chat,
    enter_chat,
    remove_member,
    leave_group,
    delete_group,
    search_user,
    accept_friend,
    reject_friend,
    delete_friend,
    cancel_request,
    toggle_theme
)

app_name = 'api'

urlpatterns = [
    path("check-new-messages/<int:id>", check_new_messages, name="check-new-messages"),
    path("send-message/", send_message, name="send-message"),
    path("delete-message/<int:id>/", delete_message, name="delete-message"),
    path("change-message/", change_message, name="change-message"),
    path("search-chat/<str:name>/", search_chat, name="search-chat"),
    path("enter-chat/<int:id>/", enter_chat, name="enter-chat"),
    path("remove-member/<int:group_id>/<int:user_id>/", remove_member, name="remove-member"),
    path("leave-group/<int:id>/", leave_group, name="leave-group"),
    path("delete-group/<int:id>/", delete_group, name="delete-group"),
    path("search-user/<str:username>/", search_user, name="search-user"),
    path("accept-friend/<int:id>/", accept_friend, name="accept-friend"),
    path("reject-friend/<int:id>/", reject_friend, name="reject-friend"),
    path("delete-friend/<int:id>/", delete_friend, name="delete-friend"),
    path("cancel-request/<int:id>/", cancel_request, name="cancel-request"),
    path("toggle-theme/<str:state>/", toggle_theme, name="toggle-theme"),
]
