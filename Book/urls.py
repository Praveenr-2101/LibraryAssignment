from django.urls import path,include
from rest_framework_simplejwt.views import (
   TokenObtainPairView,
   TokenRefreshView,
)

from . import views


urlpatterns = [
   path("Author",views.AuthorList.as_view()),
   path("Author/<int:pk>",views.AuthorDetail.as_view()),
   
   path("Books",views.BookList.as_view()),
   path("Books/<int:pk>",views.BookDetail.as_view()),
   
   
   path('borrow/', views.BorrowRecordCreateView.as_view(), name='borrow-create'),
   path('borrow/<int:pk>/return/', views.BorrowRecordReturnView.as_view(), name='borrow-return'),
   
   
   
   path('reports/', views.ReportView.as_view(), name='reports'),
   
   
   path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # 5 mintues only validate
   path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  #24 hours
]