from django.urls import path

from book.views import *

urlpatterns = [
    path('/find',FindBookView.as_view()),
    path('/filter',FilterView.as_view()),
    path('/save',SaveView.as_view()),
    path('/mypage' , MyPageView.as_view()),
    path('/user/<int:user_id>', UserPageView.as_view()),
    path('/<int:book_id>' , BookDetailView.as_view()),
    path('/<int:book_id>/comment', BookCommentView.as_view()),
]
