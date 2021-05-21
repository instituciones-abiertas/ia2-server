from rest_framework import routers
from apps.entity.views import EntityViewSet
from apps.entity.views import ActViewSet
from apps.entity.views import OcurrencyEntityViewSet
from apps.entity.views import LearningModelViewSet

ROUTER = routers.DefaultRouter()
ROUTER.register(r"entity", EntityViewSet)
ROUTER.register(r"act", ActViewSet)
ROUTER.register(r"ocurrency", OcurrencyEntityViewSet)
ROUTER.register(r"subject", LearningModelViewSet)


def get_entity_urls():
    return ROUTER.urls
