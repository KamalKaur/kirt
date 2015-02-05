from django.utils.translation import ugettext_lazy as _
from django import forms
from django.forms import TextInput, NumberInput
from django.forms import ModelForm
from src.models import *
import datetime
from src.month_choices import MONTH_CHOICES
# IMpor USer model to get the joining date of user and extract year 
# from there to be displayed in search form
from django.contrib.auth.models import User

this_year = datetime.date.today().year
user_obj = User.objects.get(is_superuser = 1)
joining_year = user_obj.date_joined.year


class SearchSelect(forms.Form):
    """
    The form is created not from any model but manualy and helps to search
    for worker records in the past. The values in two fields are coming 
    from another file i.e month_choices.py and are displayed as drop downs
    because the fields defined are Choice fields :)
    """
    year = forms.ChoiceField(label='', choices= [(year, year) for year 
        in range(joining_year, this_year+1 )])
    # this year + 1 is because For eg.range(2015, 2015) will 
    # return [] and range (2015, 2016) = 2015
    month = forms.ChoiceField(MONTH_CHOICES, label='')

class WorkerDetailForm(ModelForm):
    """
    This form is used to add any new worker and is a ModelForm.
    There are validations for input fields. All the fields are 
    mendatory to be filled.
    """

    required_css_class = 'required'
    error_css_class = 'error'
    class Meta:
        model = WorkerDetail
        exclude = ('status','resigning_date',)
        fields = '__all__'
        labels = {'first_name': (''),
            'last_name': (''),
            'address': (''),
            'joining_date': (''),
            'basic_wage': (''),
            'provident_fund': (''),
            }
        widgets = {
            'first_name': TextInput(attrs={'placeholder': 'First name'}),
            'last_name': TextInput(attrs={'placeholder': 'Last name'}),
            'address': TextInput(attrs={'placeholder': 'Address'}),
            'joining_date': TextInput(attrs={'placeholder': 'yyyy-mm-dd'}),
            'basic_wage': NumberInput(attrs={'placeholder': 'Basic wage', 'min':'0'}),
            'provident_fund': NumberInput(attrs={'placeholder': 'Provident fund', 'min':'0'}),
        }
        error_messages = {'first_name': {'max_length': ("Give proper length"),},}

class AdvanceForm(ModelForm):
    """
    Currently this form is used no where. But when the home page will 
    be changed to icons view, this form will be used to add advance 
    from outside for any worker. Using it there will prevent a worker
    from checking other's details by looking at the computer screen.
    """
    #worker_id = forms.ModelChoiceField(WorkerDetail.objects.all())
    #advance_amount = forms.IntegerField()
    #advance_date = forms.DateField(label='',initial=datetime.date.today)
    # Date field with default date in form can be added like this ^
    
    class Meta:
        model = Advance
        exclude = ('advance_date',)
        labels = {
            'worker_id': ('Worker name'),
            'advance_amount': (''),
        }
        widgets = {
            'advance_amount': NumberInput(attrs={'placeholder': 'Advance amount', 'min':'0'}),
        }
        error_messages = {'first_name': {'max_length': ("Give proper length"),},}
        # exclude = ('advance_date',) 
        # Excluding the date field but it automatically saves today's date :)
        # fields = ('worker_id', 'advance_amount')
        # The above line takes the field behaviour directly from models but how to ignore labels?

