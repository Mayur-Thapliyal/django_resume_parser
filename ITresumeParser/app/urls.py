from rest_framework.routers import DefaultRouter
from .views import *
from django.urls import path
router=DefaultRouter()
router.register('',viewset=AppView,basename='APP')
urlpatterns = [

]

urlpatterns+=router.urls