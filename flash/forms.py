from django import forms
from flash.models import CardSet, Question
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
	username = forms.CharField(label='search', widget=forms.TextInput
		(attrs={'placeholder': 'User name', 'autofocus': True, 'class': 'form-control'}))
	email = forms.CharField(label='search', widget=forms.TextInput
		(attrs={'placeholder': 'Email address', 'class': 'form-control'}))
	password = forms.CharField(widget=forms.PasswordInput
		(attrs={'placeholder': 'Password', 'class': 'form-control'}))

	class Meta:
		model = User
		fields = ['username', 'email', 'password']

class CardSetForm(forms.ModelForm):
	name = forms.CharField(max_length=48, widget=forms.TextInput(attrs=
		{'placeholder': 'Card set name', 'id': 'cardSetName', 'class':'form-control', 
		 'autofocus': True }))

	class Meta:
		model = CardSet
		fields = ['name']

class QuestionForm(forms.ModelForm):
	choice1 = forms.CharField(max_length=128, widget=forms.TextInput(
		attrs={'placeholder': 'Choice 1', 'class': 'form-control'}), required=False)
	choice2 = forms.CharField(max_length=128, widget=forms.TextInput(
		attrs={'placeholder': 'Choice 2', 'class': 'form-control'}), required=False)
	choice3 = forms.CharField(max_length=128, widget=forms.TextInput(
		attrs={'placeholder': 'Choice 3', 'class': 'form-control'}), required=False)
	choice4 = forms.CharField(max_length=128, widget=forms.TextInput(
		attrs={'placeholder': 'Choice 4', 'class': 'form-control'}), required=False)
	choice5 = forms.CharField(max_length=128, widget=forms.TextInput(
		attrs={'placeholder': 'Choice 5', 'class': 'form-control'}), required=False)
	# isAnswer1 = forms.BooleanField()
	# isAnswer2 = forms.BooleanField()
	# isAnswer3 = forms.BooleanField()
	# isAnswer4 = forms.BooleanField()
	# isAnswer5 = forms.BooleanField()

	class Meta:
		model = Question
		fields = ['question', 'choice1','choice2','choice3','choice4','choice5',
				  'isAnswer1','isAnswer2','isAnswer3','isAnswer4','isAnswer5']
		widgets = {
			'question': forms.Textarea(
				attrs={'cols': 70, 'rows': 3, 'placeholder': 'Question', 
				'class': 'form-control', 'autofocus': True }),
		}
