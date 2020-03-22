from django import forms

class AnalyticsForm(forms.Form):
    msisdn = forms.CharField(label='MSISDN', max_length=12)