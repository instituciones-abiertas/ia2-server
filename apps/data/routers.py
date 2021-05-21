from rest_framework.routers import Route, SimpleRouter
from .views import LugarStatsView, EdadStatsView, HechoStatsView


class CustomListRouter(SimpleRouter):
    routes = [
        Route(
            url=r"^{prefix}{trailing_slash}$",
            mapping={"get": "list"},
            name="{basename}",
            detail=False,
            initkwargs={"suffix": "List"},
        ),
    ]


router1 = CustomListRouter()
router1.register("lugar", LugarStatsView, "stats_lugar")


class CustomRetrieveRouter(SimpleRouter):
    routes = [
        Route(
            url=r"^{prefix}{trailing_slash}$",
            mapping={"get": "get"},
            name="{basename}",
            detail=False,
            initkwargs={"suffix": "instance"},
        ),
    ]


router2 = CustomRetrieveRouter()
router2.register("edad", EdadStatsView, "stats_edad")
router2.register("hecho", HechoStatsView, "stats_hecho")


def get_data_urls():
    return [*router1.urls, *router2.urls]
