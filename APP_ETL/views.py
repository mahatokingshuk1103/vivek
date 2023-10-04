from django.shortcuts import render, redirect
import requests
from .forms import ExcelUploadForm
from .models import Database_Siemens
import pandas as pd
from django.http import StreamingHttpResponse
import json
import random
import time
import qrcode
from django.http import HttpResponse
from .forms import WeatherForm  

def rapidapi_weather_view(request):
    '''
    Function to fetch data from RapidApi
    @request - Gets the request data
    @return - weather_data should display in rapidapi_weather_data

    '''
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


def sse_data_generator(request):
    '''
    Function to generate sse_data(IOT DATA)
    @request - Gets the request data
    @return - sse data should be generated

    '''
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


def save_data_to_database(request):
    '''
    Function to save sse data in database
    @request - Gets the request data
    @return - data should be save in database

    '''
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

                    # Create a new Database_Siemens instance and save it to the database
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


def upload_excel(request):
    '''
    Function to upload excel file
    @request - Gets the request data
    @return - display uploaded data

    '''
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
            return redirect('display_data_database')
    else:
        form = ExcelUploadForm()
    return render(request, 'upload_excel.html', {'form': form})


def generate_qr_code_view(request, item_id):
    '''
    Function to display a QR code 
    @request - Gets the request data
    @return - Data stored in a QR code 

    '''
    
    item = Database_Siemens.objects.get(pk=item_id)
    # Assuming 'item' has attributes 'time', 'temperature', and 'humidity'
    data_to_store = f"Time: {item.time}\nTemperature: {item.temperature}°C\nHumidity: {item.humidity}%"
    
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,  # set low error correction level
        box_size=10,
        border=4,
    )
    qr.add_data(data_to_store)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    response = HttpResponse(content_type="image/png")
    img.save(response, "PNG")  # save the QR code in the HTTP response in PNG format
    return response



def chart_view_graph(request):
    '''
    Function to dispaly charts
    @request - Gets the request data
    @return - data_json in graph.html

    '''
    data_points = Database_Siemens.objects.all()
    data = [{'time': point.time.strftime('%Y-%m-%d %H:%M:%S'), 
             'humidity': point.humidity,
             'temperature': point.temperature} for point in data_points]
    data_json = json.dumps(data)
    return render(request, 'graph.html', {'data_json': data_json})


def front_view(request):
    '''
    Function to display front page of website
    @request - Gets the request data
    @return -  render to front.html
     
    '''
    return render(request, 'front.html')


def display_data_database(request):
    '''
    Function to display data of Database_Siemens
    @request - Gets the request data
    @return - data in display_data.html
     
    '''
    data = Database_Siemens.objects.all().order_by('-time')
    return render(request, 'display_data.html', {'data': data})
