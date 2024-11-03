from django.contrib.postgres.search import (
    SearchQuery,
    SearchRank,
    SearchVector,
    SearchHeadline,
)

from users.models import User, Chat


def user_search(query):
    vector = SearchVector("imie", "nazwisko")
    query = SearchQuery(query)

    result = (
        User.objects.annotate(rank=SearchRank(vector, query))
        .filter(rank__gt=0.01)
        .order_by("-rank")
    )
    return result


def chat_search(query):
    # vector = SearchVector("nazwa")
    # query = SearchQuery(query)

    # result = (
    #     Chat.objects.annotate(rank=SearchRank(vector, query))
    #     .filter(rank__gt=0)
    #     .order_by("-rank")
    # )
    # return result
    return Chat.objects.filter(nazwa__icontains=query)