from typing import TypeVar, Generic

from django.db.models import Model
from rest_framework.views import APIView

from dry_django.contrib.rest_framework.mixins import (
    ApiDefaultMixin,
    ModelListAPIMixin,
    ModelRetrieveAPIMixin,
    ModelCreateAPIMixin,
    ModelUpdateAPIMixin,
    ModelDestroyAPIMixin,
)


class DefaultAPIView(ApiDefaultMixin, APIView):
    """
    Базовый класс для создания представлений, включающий миксины по умолчанию
    """

    pass


###################################
#  Generic Dry Django views
###################################

_DjangoModelTypeVar = TypeVar("_DjangoModelTypeVar", bound=Model)


class ModelListAPIView(ModelListAPIMixin, DefaultAPIView, Generic[_DjangoModelTypeVar]):
    pass


class ModelListCreateAPIView(
    ModelListAPIMixin, ModelCreateAPIMixin[_DjangoModelTypeVar], DefaultAPIView, Generic[_DjangoModelTypeVar]
):
    pass


class ModelRetrieveUpdateDestroyAPIView(
    ModelRetrieveAPIMixin[_DjangoModelTypeVar],
    ModelUpdateAPIMixin[_DjangoModelTypeVar],
    ModelDestroyAPIMixin[_DjangoModelTypeVar],
    DefaultAPIView,
    Generic[_DjangoModelTypeVar],
):
    pass
