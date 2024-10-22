from django.contrib.postgres.search import (
    SearchQuery,
    SearchRank,
    SearchVector,
    SearchHeadline,
)

from users.models import User


def q_search(query):
    # if query.isdigit() and len(query) <= 5:
    #     return User.objects.filter(id=int(query))

    vector = SearchVector("imie", "nazwisko")
    query = SearchQuery(query)

    result = (
        User.objects.annotate(rank=SearchRank(vector, query))
        .filter(rank__gt=0)
        .order_by("-rank")
    )
    result = result.annotate(
        headline=SearchHeadline(
            "imie",
            query,
            start_sel='<span style="background-color: yellow">',
            stop_sel="</span>",
        )
    )
    result = result.annotate(
        bodyline=SearchHeadline(
            "nazwisko",
            query,
            start_sel='<span style="background-color: yellow">',
            stop_sel="</span>",
        )
    )

    return result