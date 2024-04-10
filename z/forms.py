from django.contrib.gis import forms

from .models import Treasure

class CustomOpenLayersWidget(forms.OpenLayersWidget):
    template_name = 'z/openlayers.html'

class CustomOSMWidget(forms.OSMWidget):
    template_name = 'z/openlayers-osm.html'

class TreasurePostForm(forms.ModelForm):

    class Meta:
        model = Treasure
        fields = ['location', 'description']
        widgets = {
            'location': CustomOSMWidget(attrs={'default_lon': 37.618423, 'default_lat': 55.751244}),
        }
    
    class Media:
        css = {'screen and (min-aspect-ratio:1)': ['z/styles/treasure_form.css']}

