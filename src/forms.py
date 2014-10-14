from django.utils.translation import ugettext_lazy as _
from django import forms
from django.forms import ModelForm
from src.models import *
import datetime
from src.month_choices import MONTH_CHOICES

class SearchSelect(forms.Form):
    """
    This is the search form.
    """
    year = forms.ChoiceField(choices= [(datetime.date.today().year, datetime.\
    date.today().year)] + [(x, x) for x in range(2000, 2050)])
    month = forms.ChoiceField(MONTH_CHOICES)

class WorkerDetailForm(ModelForm):
    """
    This form is used to add any new worker, is a ModelForm
    """
    class Meta:
        model = WorkerDetail
        fields = '__all__'
        error_messages = {'first_name': {'max_length': ("Give proper length"),},}

class AdvanceForm(ModelForm):
    """
    This form is used no where now, But just kept it as a piece of History!
    Looks beautiful as shows how I worked here :D
    """
    worker_id = forms.ModelChoiceField(WorkerDetail.objects.all())
    advance_amount = forms.IntegerField()
    # advance_date = forms.DateField(label='',initial=datetime.date.today)
    # Date field with default date in form can be added like this ^
    
    class Meta:
        model = Advance
        # exclude = ('advance_date',) 
        # Excluding the date field but it automatically saves today's date :)
        # fields = ('worker_id', 'advance_amount')
        # The above line takes the field behaviour directly from models but how to ignore labels?

