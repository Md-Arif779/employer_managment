from django.urls import path
from .import views
from .views import commentdelete,notification, posts, PostListView, post_details,search,addcomment,PostCreateView



urlpatterns = [
    path('posts/',posts,name="posts"),
   
    path('search/',search,name="search"),
    path('addcomment/',addcomment,name="addcomment"),
    path('commentdelete/<int:pk>/',commentdelete, name="commentdelete"),
    path('postlist/',PostListView.as_view(),name="postlist"),
    path('post/details/<int:pk>', post_details, name='postdetails'),
    # path('edit/<int:pk>',PostEditView.as_view() , name='edit'),
    # path('delete/<int:pk>',PostDeleteView.as_view() , name='delete'),
    # path('postcreate/',postcreate,name="postcreate"),
    path('create/',PostCreateView.as_view(),name="create"),
    path('edit/<int:pk>/',views.UpdateEdit, name="edit"),
    path('delete/<int:pk>/',views.PostDeleteView.as_view(), name="delete"),
    path('notification/',notification,name="notification"),   
       
]

