from django.shortcuts import render, redirect
import requests
from .forms import ExcelUploadForm
from .models import Database_Siemens
import pandas as pd
from django.http import JsonResponse, StreamingHttpResponse
import json
import random
import time
import qrcode
from django.http import HttpResponse
from io import BytesIO
from PIL import Image
from .forms import WeatherForm  # Import your form

def rapidapi_weather_view(request):
    if request.method == 'POST':
        form = WeatherForm(request.POST)
        if form.is_valid():
            latitude = form.cleaned_data['latitude']
            longitude = form.cleaned_data['longitude']

            url = "https://weatherapi-com.p.rapidapi.com/current.json"
            querystring = {"q": f"{latitude},{longitude}"}
            headers = {
                "X-RapidAPI-Key": "91477e6fddmshcbf946191cad483p11feccjsnfeeea016c013",
                "X-RapidAPI-Host": "weatherapi-com.p.rapidapi.com"
            }

            response = requests.get(url, headers=headers, params=querystring)
            weather_data = response.json()

            return render(request, 'rapidapi_weather_data.html', {'weather_data': weather_data})

    else:
        form = WeatherForm()

    return render(request, 'weather_form.html', {'form': form})








#SSE Data Generator vIEW

def sse_data_generator(request):
    def event_stream():
        while True:
            data = {
                'time': time.strftime("%Y-%m-%d %H:%M:%S"),
                'humidity': round(random.uniform(30, 70), 2),  # Simulate humidity data
                'temperature': round(random.uniform(18, 28), 2),  # Simulate temperature data
            }
            yield f"{json.dumps(data)}\n\n"
            time.sleep(3)  # Adjust the interval as needed

    response = StreamingHttpResponse(event_stream(), content_type="text/event-stream")
    response['Cache-Control'] = 'no-cache'
    return response 

    
#SSE DATA STORING AND DISPLAYING IN UI

def save_data_to_database(request):
    url = 'http://127.0.0.1:8000/sse_gen/'  # Replace with your actual URL

    def data_generator():
        response = requests.get(url, stream=True)

        if response.status_code == 200:
            for line in response.iter_lines(decode_unicode=True):
                if line:
                    data = json.loads(line)
                    
                    # Extract data from the JSON response
                    time = data['time']
                    humidity = data['humidity']
                    temperature = data['temperature']

                    # Create a new SensorData instance and save it to the database
                    sensor_data = Database_Siemens(
                        time=time,
                        humidity=humidity,
                        temperature=temperature
                    )
                    sensor_data.save()

                    yield f'Data saved: {sensor_data}\n'
                
        else:
            yield f'Failed to fetch data from URL. Status code: {response.status_code}\n'

    return StreamingHttpResponse(data_generator(), content_type='text/plain')
    


#Excel Upload view 
def upload_excel(request):
    if request.method == 'POST':
        form = ExcelUploadForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = request.FILES['excel_file']
            df = pd.read_excel(excel_file)
            for index, row in df.iterrows():
                Database_Siemens.objects.create(time=row['time'], 
                                         humidity=row['humidity'], 
                                         temperature=row['temperature'], 
                                         )
            return redirect('display_data')
    else:
        form = ExcelUploadForm()
    return render(request, 'upload_excel.html', {'form': form})


#QR CODE SHOW   
def generate_qr_code_view(request, item_id):
    item = Database_Siemens.objects.get(pk=item_id)
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(item.time)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    response = HttpResponse(content_type="image/png")
    img.save(response, "PNG")
    return response





#GRAPH View

def chart_view_graph(request):
    data_points = Database_Siemens.objects.all()
    data = [{'time': point.time.strftime('%Y-%m-%d %H:%M:%S'), 'humidity': point.humidity, 'temperature': point.temperature} for point in data_points]
    data_json = json.dumps(data)
    return render(request, 'graph.html', {'data_json': data_json})


#FRONT View
def front_view(request):
    return render(request, 'front.html')

#Excel data show view
def display_data_database(request):
    data = Database_Siemens.objects.all().order_by('-time')
    return render(request, 'display_data.html', {'data': data})






















 
