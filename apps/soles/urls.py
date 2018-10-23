from django.urls import path
#DO this!!!!! up above
from . import views

urlpatterns = [
    path('', views.index),
    path('validate',views.validate),
    path('log',views.log),
    path('dashboard',views.dash),
    path('review', views.review),
    path('createreview', views.create_review),
    path('about', views.about),
    path('find_shoes', views.search_shoes),
    path('logout', views.logout),
    path('edit/<int:id>', views.edit),
    path('delete/<int:id>', views.delete_post),
    path('update/<int:id>', views.update_post),
    path('view/<int:id>', views.display_post),
    path('profile', views.go_profile),
    path('profile/<int:id>', views.get_pofile),
    path('profile/edit', views.edit_prof),
    path('update/user/<int:id>', views.update_user),
]