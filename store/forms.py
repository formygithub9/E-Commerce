from django import forms

class Contact_Form(forms.Form):
    Name=forms.CharField(label='Name',max_length=100)
    email=forms.EmailField(label='Email',max_length=200)
    subject=forms.CharField(label='Subject',max_length=500)
    message=forms.CharField(label='Your Message',widget=forms.Textarea)