from django.db import models
from django.contrib.auth.models import User

class CardSet(models.Model):
	name = models.CharField(max_length=128)
	user = models.ForeignKey(User)
	isPublic = models.BooleanField(default=False)

	def __unicode__(self):
		return self.name

class Question(models.Model):
	question = models.TextField()
	questionType = models.CharField(max_length=24, blank=True)
	cardSet = models.ForeignKey(CardSet, blank=True)
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

	def __unicode__(self):
		return str(self.pk)

class UserProfile(models.Model):
	user = models.OneToOneField(User)

	website = models.URLField(blank=True)
	picture = models.ImageField(upload_to='profile_images', blank=True)

	def __unicode__(self):
		return self.user.username