
from rest_framework.routers import DefaultRouter
from .views import BaseView

base_router = DefaultRouter()
base_router.register(r"base", viewset=BaseView, basename="base")