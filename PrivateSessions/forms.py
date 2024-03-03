from django import forms

from PrivateSessions.models import PrivateSessionRequest


class PrivateSessionRequestForm(forms.ModelForm):
    selected_professor = forms.ChoiceField(label='Professor Selector', choices=PrivateSessionRequest.PROFESSOR_CHOICES)
    session_mode = forms.ChoiceField(label='Session Mode', choices=PrivateSessionRequest.TYPES, required=False)
    first_name = forms.CharField(label='First Name', max_length=50, required=False)
    last_name = forms.CharField(label='Last Name', max_length=50, required=False)
    email = forms.EmailField(label='Email', max_length=254, required=False)
    phone = forms.CharField(label='Phone Number', max_length=50, required=False)
    duration_hours = forms.ChoiceField(label='Duration Hours', choices=PrivateSessionRequest.DURATION_CHOICES, required=False)

    class Meta:
        model = PrivateSessionRequest
        fields = []  # empty fields as we have defined them explicitly


class PrivateSessionForm(forms.Form):
    first_name = forms.CharField(label='First Name', max_length=100)
    last_name = forms.CharField(label='Last Name', max_length=100)
    email = forms.EmailField(label='Email')
    phone_number = forms.CharField(label='Phone Number', max_length=15)
    session_time = forms.ChoiceField(label='Session Time', choices=[
        (30, '30 Minutes'),
        (60, '1 Hour'),
        (90, '1H 30 Minutes'),
        (120, '2 Hours'),
    ])
    session_mode = forms.ChoiceField(label='Session Mode', choices=[
        (0, 'a session by yourself alone'),
        (1, 'a session just between you and your friends'),
        (2, 'a session including you and another group'),
    ])
    professor_selector = forms.ChoiceField(label='Professor Selector', choices=[
        (0, 'az'),
        (1, '1 zz'),
        (2, '1H 30zz Minutes'),
    ])