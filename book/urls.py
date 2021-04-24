from django.urls import path

from book.views import FindBookView

urlpatterns = [
    path('/find',FindBookView.as_view()),
]