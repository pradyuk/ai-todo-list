from django.urls import path, include
from rest_framework.routers import DefaultRouter
from todo.views import EmployeeViewSet, TaskViewSet, CommentViewSet

router = DefaultRouter()
router.register(r"employees", EmployeeViewSet)
router.register(r"tasks", TaskViewSet)
router.register(r"comments", CommentViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
