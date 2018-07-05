from django import forms
import datetime

from .models import Input


YEAR_CHOICES = ('2014', '2015', '2016', '2017', '2018', '2019', '2020')


class TatForm(forms.ModelForm):
    start_date = forms.DateField(initial=datetime.date.today, widget=forms.SelectDateWidget(years=YEAR_CHOICES), required=False)
    end_date = forms.DateField(initial=datetime.date.today, widget=forms.SelectDateWidget(years=YEAR_CHOICES), required=False)

    class Meta:
        model = Input
        fields = ('start_date', 'end_date')
