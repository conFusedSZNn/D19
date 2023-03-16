
from django.urls import path
from .views import PostList, PostCreate, PostEdit, PostDetail, D19LoginView, RegisterUserView, D19LogoutView


urlpatterns = [
    path('',  PostList.as_view(), name= 'home'),
    path('detail/<int:pk>', PostDetail.as_view(), name= 'detail_page'),
    path('edit-page', PostCreate.as_view(), name= 'edit_page'),
    path('updade-page/<int:pk>', PostEdit.as_view(), name= 'update_page'),
    path('login', D19LoginView.as_view(), name='login_page'),
    path('registrate',RegisterUserView.as_view(), name='register_page'),
    path('logout', D19LogoutView.as_view(), name='logout_page'),
]
