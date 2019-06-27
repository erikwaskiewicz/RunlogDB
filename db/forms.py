from django import forms
import datetime
#from .models import Input


# Form for inputting start and end dates for turn around time queries. Saves inputs to the Input model, but this isn't committed to the database.
YEAR_CHOICES = ('2014', '2015', '2016', '2017', '2018', '2019', '2020')

class TatForm(forms.Form):
    start_date = forms.DateField(initial=datetime.date.today, widget=forms.SelectDateWidget(years=YEAR_CHOICES), required=False)
    end_date = forms.DateField(initial=datetime.date.today, widget=forms.SelectDateWidget(years=YEAR_CHOICES), required=False)

#    class Meta:
#        model = Input
#        fields = ('start_date', 'end_date')


# Form for inputting search queries to search the database. Saves inputs to the Input model, but this isn't committed to the database.
class SearchForm(forms.Form):
    run_id = forms.CharField(required=False, label='Run ID')
    experiment = forms.CharField(required=False, label='Worksheet ID')
    samples = forms.CharField(required=False, label='Sample ID', widget=forms.TextInput())
    pipeline = forms.CharField(required=False, label='Pipeline')

#    class Meta:
#        model = Input
#        fields = ('run_id', 'experiment', 'samples', 'pipeline')