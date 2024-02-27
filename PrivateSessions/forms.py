from django import forms

class PrivateSessionForm(forms.Form):
    first_name = forms.CharField(label='First Name', max_length=100)
    last_name = forms.CharField(label='Last Name', max_length=100)
    email = forms.EmailField(label='Email')
    phone_number = forms.CharField(label='Phone Number', max_length=15)
    session_time = forms.ChoiceField(label='Session Time', choices=[
        ('30Min', '30 Minutes'),
        ('60Min', '1 Hour'),
        ('90Min', '1H 30 Minutes'),
        ('120Min', '2 Hours'),
    ])
    session_mode = forms.ChoiceField(label='Session Mode', choices=[
        ('Mode1', 'A session by yourself alone'),
        ('Mode2', 'A session just between you and your friends'),
        ('Mode3', 'A session including you and another group'),
    ])
    professor_selector = forms.ChoiceField(label='Professor Selector', choices=[
        ('Adem', 'Professor 1'),
        ('Oussama', 'Professor 2'),
        ('Iyed', 'Professor 3'),
    ])