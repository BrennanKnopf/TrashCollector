from django.urls import path

from . import views

# TODO: Determine what distinct pages are required for the user stories, add a path for each in urlpatterns

app_name = "employees"
urlpatterns = [
    path('', views.index, name="index"),
    path('new/', views.create, name="create"),
    path('edit_profile/', views.edit_profile, name="edit_profile"),
    path('<int:customer_id>/',views.pick_up, name="pick_up"),
    path('week_filter/<str:weekly_pickup>/', views.week_filter, name="week_filter")


]