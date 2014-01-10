from django.db import models
from django.contrib.auth.models import User

class CardSet(models.Model):
	ME = 'me'
	EVERYONE = 'eo'
	PEOPLE_WTH_PW = 'pw'
	VISIBLE_TO = (
		('me', 'just me'),
		('eo', 'everyone'),
		('pw', 'people with a password...')
	)
	name = models.CharField(max_length=48)
	user = models.ForeignKey(User)
	visibleTo = models.CharField(max_length=2, choices=VISIBLE_TO, default=ME)
	created = models.DateTimeField(auto_now_add=True)
	lastModified = models.DateTimeField(auto_now=True)
	view = models.IntegerField(default=0)
	password = models.CharField(max_length=24, null=True, blank=True)

	def __unicode__(self):
		return self.name

	def numberOfQuestions(self):
		return self.question_set.count() 

class Question(models.Model):
	question = models.TextField()
	questionType = models.CharField(max_length=24, blank=True)
	cardSet = models.ForeignKey(CardSet, blank=True)
	created = models.DateTimeField(auto_now_add=True)
	lastModified = models.DateTimeField(auto_now=True)
	choice1 = models.CharField(max_length=128, null=True, blank=True)
	choice2 = models.CharField(max_length=128, null=True, blank=True)
	choice3 = models.CharField(max_length=128, null=True, blank=True)
	choice4 = models.CharField(max_length=128, null=True, blank=True)
	choice5 = models.CharField(max_length=128, null=True, blank=True)
	isAnswer1 = models.BooleanField(default=False)
	isAnswer2 = models.BooleanField(default=False)
	isAnswer3 = models.BooleanField(default=False)
	isAnswer4 = models.BooleanField(default=False)
	isAnswer5 = models.BooleanField(default=False)

	def __unicode__(self):
		return self.question

class Test(models.Model):
	user = models.ForeignKey(User)
	questions = models.ManyToManyField(Question)
	created = models.DateTimeField(auto_now_add=True)
	lastModified = models.DateTimeField(auto_now=True)

	def __unicode__(self):
		return str(self.pk)

class UserProfile(models.Model):
	user = models.OneToOneField(User)

	website = models.URLField(blank=True)
	picture = models.ImageField(upload_to='profile_images', blank=True)

	def __unicode__(self):
		return self.user.username