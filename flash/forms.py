from django import forms
from flash.models import CardSet, Question
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
	username = forms.CharField(help_text="Please enter a username.")
	email = forms.CharField(help_text="Please enter your email.")
	password = forms.CharField(widget=forms.PasswordInput(), help_text="Please enter a password.")

	class Meta:
		model = User
		fields = ['username', 'email', 'password']

class CardSetForm(forms.ModelForm):
	name = forms.CharField(max_length=128, help_text="Please enter a Card Set name.")
	#isPublic = forms.BooleanField(help_text="If checked, this card set will be publicly available.")

	class Meta:
		model = CardSet
		fields = ['name', 'isPublic']

class QuestionForm(forms.ModelForm):
	# choice1 = forms.CharField(max_length=128, help_text="Choice1")
	# choice2 = forms.CharField(max_length=128, help_text="Choice2")
	# choice3 = forms.CharField(max_length=128, help_text="Choice3")
	# choice4 = forms.CharField(max_length=128, help_text="Choice4")
	# choice5 = forms.CharField(max_length=128, help_text="Choice5")
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
			'question': forms.Textarea(attrs={'cols': 70, 'rows': 3}),
		}
