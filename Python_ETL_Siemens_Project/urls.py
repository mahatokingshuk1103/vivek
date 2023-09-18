"""
URL configuration for Python_ETL_Siemens_Project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from APP_ETL.views import upload_excel,front_view,display_data_database,generate_qr_code_view,chart_view_graph,sse_data_generator,save_data_to_database,rapidapi_weather_view

urlpatterns = [
    path('admin/', admin.site.urls),
    
    #Excell urls
    path('excel_upload/', upload_excel, name='upload_excel'),
    

    #SSE Data Generator
    path('sse_gen/', sse_data_generator , name='sse_data_generator'),

    #Storing SSE DATA AND SHOWING
    path('sse_save/', save_data_to_database ,name='save_data_to_database'),
    


    #RAPIDAPI DATA DISPLAY 
    path('rapid_show/',rapidapi_weather_view, name='rapidapi_weather_view'),


    #QR CODE GENERATOR
    path('generate_qr/<int:item_id>/', generate_qr_code_view, name='generate_qr_code'),


    #GRAPH View
    
    path('graph/',chart_view_graph, name='chart_view_graph'),
    
    

    #Front page 
    path('',front_view, name='front_view'),

    #Data show 
    path('show_data/',display_data_database, name='display_data_database'),
    

]
