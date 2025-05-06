from django.urls import path
from . import views
app_name = 'home'

urlpatterns = [
    #path('home/', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact_view, name='contact_view'),
    path("success_page/", views.success_page, name="success_page"),
    
    # path('services/', views.services, name='services'),
    # path('portfolio/', views.portfolio, name='portfolio'),
    # path('blog/', views.blog, name='blog'),
    # path('testimonials/', views.testimonials, name='testimonials'),
    # path('faq/', views.faq, name='faq'),
    # path('new-feature/', views.new_feature, name='new_feature'),
    # path('events/', views.events, name='events'),
    # path('feedback/', views.feedback, name='feedback'),
    # path('team/', views.team, name='team'),
    # path('careers/', views.careers, name='careers'),
]