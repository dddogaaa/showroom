from django.urls import path, include
from .views import HomepageView,ProductpageView,ProductpageDetail,AboutUsPage

urlpatterns = [
    path('', HomepageView.as_view(), name='homepage'),
    path('urunler/', ProductpageView.as_view(), name='productspage'),
    path('urun/<slug:slug>', ProductpageDetail.as_view(), name='productspage_detail'),
    path('hakkimizda/', AboutUsPage.as_view(), name='aboutus'),



    #Ckeditor
    path('ckeditor5/', include('django_ckeditor_5.urls')),


]
