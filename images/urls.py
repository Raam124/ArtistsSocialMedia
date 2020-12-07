from django.urls import path 
from images.views import *



urlpatterns = [
    path("home", homepage, name="home"),
    path("<slug>/detail",picture_detail, name = "picture_detail"),
    # path("about_us/", about_us, name="about_us"),
    # path("terms_of_use/", terms_of_use, name="terms_of_use"),
    # path("privacy_policy/", privacy_policy, name="privacy_policy"),
    # path('tag/<slug:tag_slug>/',homepage, name='post_list_by_tag'),
    # path('contactus',contactus, name='contactus'),


    path('like/',image_like, name='like'),

    path('create_ad', create_image_post, name='create_image_post'),
    path('<slug>/edit', edit_image_post_view, name='edit_image_post_view'),
    path('<slug>/delete', delete_image_post_view, name='delete_image_post_view'),
]
