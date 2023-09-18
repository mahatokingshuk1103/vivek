from django import forms
from .models import Database_Siemens

class ExcelUploadForm(forms.Form):
    excel_file = forms.FileField()




class ItemForm(forms.ModelForm):
    class Meta:
        model = Database_Siemens
        fields = ['time','humidity','temperature']



class WeatherForm(forms.Form):
    latitude = forms.DecimalField(
        label='Latitude',
        max_digits=9,  # Set maximum digits allowed for latitude
        decimal_places=6,  # Set decimal places allowed for latitude
        required=True,
    )
    longitude = forms.DecimalField(
        label='Longitude',
        max_digits=9,  # Set maximum digits allowed for longitude
        decimal_places=6,  # Set decimal places allowed for longitude
        required=True,
    )
