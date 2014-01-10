from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from random import randint

from flash.models import CardSet, Question, Test
from flash.forms import UserForm, CardSetForm, QuestionForm

SHORT_ANSWER = 'Short answer'
MULTIPLE_CHOICE = 'Multiple choice'
ALL_THAT_APPLY = 'All that apply'

def index(request):
	backgroundList = ["#4CE59C", "#628DDA", "#32C50E", "#EA60F0", "#E75223", "#F0EA60",
					"#60CDF0", "#FDFD00", "#FD0047", "#039E8B"]
	background = backgroundList[randint(0, len(backgroundList) -1)]

	context = RequestContext(request)
	cardSetList = CardSet.objects.order_by('-created')[:20]

	context_dict = {'cardSetList': cardSetList, 'background': background }
	return render_to_response('flash/index.html', context_dict, context)

def example(request):
	context = RequestContext(request)
	return render_to_response('flash/example.html', context)

############## Authentication ##############################

def register(request):
	context = RequestContext(request)
	registered = False
	message = ""

	if request.method == 'POST':
		userForm = UserForm(data=request.POST)
		if userForm.is_valid():
			user = userForm.save()
			confirm = request.POST['confirm']
			if confirm.strip()  == user.password:
				user.set_password(user.password)
				user.save()
				registered = True
			else:
				message = "Confirmed password and password have to be the same."
		else:
			print userForm.errors
	else:
		userForm = UserForm()
	if registered:
		message = "Thanks for registering!"
	
	return render_to_response(
		'flash/register.html',
		{'userForm': userForm, 'registered': registered, 'message': message},
		  context)

def userLogin(request):
	context = RequestContext(request)
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
				return HttpResponseRedirect('/dashboard/0/0')
			else:
				return HttpResponse("Your FlashCard account is disabled.")
		else:
			return render_to_response('flash/login.html', {'error': True}, context)
	else:
		return render_to_response('flash/login.html', {}, context)

@login_required
def userLogout(request):
	logout(request)
	return HttpResponseRedirect('/')

#####################   Create and Edit    ######################

@login_required
def addQuestion(request, cardset_id):
	context = RequestContext(request)
	message = ""
	questionType = ""
	if request.method == 'POST':
		questionForm = QuestionForm(request.POST)
		#It the question field is filled out, it is valid.
		if questionForm.is_valid():
			question = questionForm.save(commit=False)
			question, questionType = classifyQuestionType(question)
			if questionType != "Invalid":
				question.questionType = questionType
				question.cardSet = CardSet.objects.get(pk=cardset_id)
				question.save()
				question.cardSet.save()
				#Refresh to new form			
				questionForm = QuestionForm()
				message = "Question successfully created."
				questionType = "The questionType is: " + questionType
			else:
				questionType = "The Question is invalid"
		else:
			print questionForm.errors
	else:
		questionForm = QuestionForm()
	
	context_dict = {'questionForm': questionForm, 'message': message, 
					'cardset_id': cardset_id, 'questionType': questionType}
	return render_to_response('flash/addQuestion.html', context_dict, context)

@login_required
def editQuestion(request, question_id):
	context = RequestContext(request)
	question = Question.objects.get(pk=question_id)
	cardSetList = CardSet.objects.filter(user=request.user)

	message = ""
	questionType = ""
	if request.method == 'POST':
		questionForm = QuestionForm(request.POST, instance=question)
		if questionForm.is_valid():
			question = questionForm.save(commit=False)
			question, questionType = classifyQuestionType(question)
			if questionType != "Invalid":
				question.questionType = questionType
				selectedCardSet = request.POST['cardSet']
				question.cardSet = CardSet.objects.get(name=selectedCardSet)
				question.save()
				question.cardSet.save()
				message = "Question successfully edited."
				questionType = "The questionType is: " + questionType
			else:
				questionType = "The Question is invalid"
		else:
			print questionForm.errors
	else:
		questionForm = QuestionForm(instance=question)
	
	context_dict = {'questionForm': questionForm, 'message': message, 'question': question,
					'questionType': questionType, 'cardSetList': cardSetList}
	return render_to_response('flash/editQuestion.html', context_dict, context)


@login_required
def dashboard(request, cardset_id, option):
	context = RequestContext(request)
	cardSetList = CardSet.objects.filter(user=request.user).order_by('-lastModified')
	message, form = "", ""

	try:
		selectedCardSet = CardSet.objects.get(pk=cardset_id)
		questionList = Question.objects.filter(cardSet=selectedCardSet).order_by('-lastModified')
	except: #DoesNotExist
		# selectedCardSet, questionList = None, None
		try: #Get the most recent updated cardset	
			selectedCardSet = CardSet.objects.filter(user=request.user).order_by('-lastModified')[0]
			questionList = selectedCardSet.question_set.all().order_by('-lastModified')
			cardset_id = selectedCardSet.pk
		except:
			print "You have no card set yet."
			message = "You have no card set yet."
			selectedCardSet, questionList = None, None

	if option == "create": #Create a new card set
		if request.method == 'POST':
			form = CardSetForm(request.POST)
			visibleTo = request.POST['visibleTo']
			password = request.POST['password'].strip()	
			if form.is_valid():
				selectedCardSet = form.save(commit=False)
				if not(visibleTo == "pw" and password == ""):
					selectedCardSet.user = request.user
					selectedCardSet.visibleTo = visibleTo
					selectedCardSet.password = password
					selectedCardSet.save()
					cardset_id = selectedCardSet.pk
					message = "Card Set successfully created."
					#return redirect('/dashboard/' + str(cardSet.id))
				else:
					message = "Password is required."
			else:
				print form.errors
		else:
			form = CardSetForm()
			selectedCardSet = None

	elif option == "edit": #Edit a selected card set
		if request.method == 'POST':
			form = CardSetForm(request.POST, instance=selectedCardSet)
			visibleTo = request.POST['visibleTo']
			password = request.POST['password'].strip()	
			if form.is_valid():
				selectedCardSet = form.save(commit=False)
				if not(visibleTo == "pw" and password == ""):
					selectedCardSet.user = request.user
					selectedCardSet.visibleTo = visibleTo
					selectedCardSet.password = password
					selectedCardSet.save()
					cardset_id = selectedCardSet.pk
					message = "Card Set successfully created."
					#return redirect('/dashboard/' + str(cardSet.id))
				else:
					message = "Password is required."
			else:
				print form.errors
		else:
			form = CardSetForm(instance=selectedCardSet)
	elif option == "delete":
		message = selectedCardSet.name + " deleted."
		selectedCardSet.delete()
		option, cardset_id = "0", "0"
		selectedCardSet, questionList = None, None
		return HttpResponseRedirect('/dashboard/0/0')
		
	context_dict = {'cardSetList': cardSetList, 'questionList': questionList,
					'selectedCardSet': selectedCardSet, 'message': message, 'form': form,
					'cardset_id': cardset_id, 'option': option}
	return render_to_response('flash/dashboard.html', context_dict, context)



###################  Test  #################################

@login_required
def test(request, test_id, cardset_id, question_id, option=None):
	context = RequestContext(request)
	message, answerBack, disabled, questionCount, incorrects = "", "", "", "", ""
	checked = ["","","","",""]
	user = request.user
	if request.method == 'POST':
		question = Question.objects.get(pk=question_id)
		if question.questionType == SHORT_ANSWER:
			answerBack = request.POST['answer'].strip()
			answer = findAnswerForSA(question)
			message = "Correct!" if answerBack.lower() == answer.lower() else "Try again!"
		elif question.questionType == MULTIPLE_CHOICE:
			answerBack = request.POST['answer']
			checked[int(answerBack) -1] = "checked"
			answer = findAnswerForMC(question)
			message = "Correct!" if answerBack == answer else "Try again!"
		elif question.questionType == ALL_THAT_APPLY:
			answerBackList = request.POST.getlist('answer')
			answerList = findAnswerForAA(question)
			correct = True
			for answer in answerBackList:
				checked[int(answer) -1] = "checked"
				if not answer in answerList:
					correct = False
			if len(answerBackList) != len(answerList):
				correct = False
			message = "Correct!" if correct == True else "Try again!"
	else: #GET
		if option == "1": #View answer
			print "View answer called"
			question = Question.objects.get(pk=question_id)
			if question.questionType == SHORT_ANSWER:
				answer = findAnswerForSA(question)
				answerBack = answer
			elif question.questionType == MULTIPLE_CHOICE:
				answer = findAnswerForMC(question)
				checked[int(answer) -1] = "checked"	
			else:
				answerList = findAnswerForAA(question)
				for i in answerList:
					checked[int(i) -1] = "checked"

			test = Test.objects.get(pk=test_id)
			test.questions.remove(question)
			nextTestId = request.session.get('nextTestId')
			if nextTestId != 0: #Does next test already exist?
				nextTest = Test.objects.get(pk=nextTestId)
			else:
				#Create a new test that consists of questions user gave up
				nextTest = Test(user=user)
				nextTest.save()
				request.session['nextTestId'] = nextTest.pk
			print request.session['nextTestId']
			nextTest.questions.add(question)
			#Disable the submission button so user can't select it anymore.
			disabled = "disabled" 
		elif option == "2": #Next question
			print "Next question called"
			question = Question.objects.get(pk=question_id)
			test = Test.objects.get(pk=test_id)
			test.questions.remove(question)
			correct = request.session.get('correct') 
			if correct == 0: #Previoud answer was incorrect
				nextTestId = request.session.get('nextTestId')
				if nextTestId != 0: #Does next test already exist?
					nextTest = Test.objects.get(pk=nextTestId)
				else:
					#Create a new test that consists of questions user gave up
					nextTest = Test(user=user)
					nextTest.save()
					request.session['nextTestId'] = nextTest.pk
				print request.session['nextTestId']
				nextTest.questions.add(question)

			try:
				question = Question.objects.filter(test=test).order_by('?')[0]
			except IndexError: #Test is empty. Move on to next test
				print "Index error called"
				test.delete()
				nextTestId = request.session.get('nextTestId')
				test = Test.objects.get(pk=nextTestId)
				test_id = test.id
				request.session['nextTestId'] = 0
				question = Question.objects.filter(test=test).order_by('?')[0]
			request.session['correct'] = 0

		else: #New test
			print "New test called"
			Test.objects.filter(user=user).delete()
			request.session['nextTestId'] = 0
			request.session['correct'] = 0
			cardSet = CardSet.objects.get(pk=cardset_id)
			test = Test(user=user)
			test.save()
			test_id = test.id
			questionList = Question.objects.filter(cardSet=cardSet)
			for question in questionList:
				test.questions.add(question)

			# Randomly select one question from current test.
			# test(yes, lower case) here refers to Test objects in general, 
			# not the test object initialized above.
			question = Question.objects.filter(test=test_id).order_by('?')[0]

	questionCount = Question.objects.filter(test=test_id).count()
	nextTestId = request.session.get('nextTestId')
	if questionCount == 1 and nextTestId == 0:
		nextQuestion = 0
	else: 
		nextQuestion = 1
	# Remove the question from test so it won't be selected next time.
	if message == "Correct!":
		test = Test.objects.get(pk=test_id)
		test.questions.remove(question)
		request.session['correct'] = 1
		disabled = "disabled" 
	else:
		request.session['correct'] = 0
		
	
	questionCount = Question.objects.filter(test=test_id).count()
	incorrects = Question.objects.filter(test=nextTestId).count()

	context_dict = {'cardSetId': cardset_id,'testId': test_id, 'question': question,
		 			'message': message, 'answerBack': answerBack, 'checked': checked,
		 			'disabled': disabled, 'nextQuestion': nextQuestion,
		 			'questionCount': questionCount, 'incorrects': incorrects}
	return render_to_response('flash/test.html', context_dict, context)


################## Helper function for create and edit card set #############




################## Helper functions for test #####################

def findAnswerForSA(question):
	if question.choice1 != "":
		answer = question.choice1
	elif question.choice2 != "":
		answer = question.choice2
	elif question.choice3 != "":
		answer = question.choice3
	elif question.choice4 != "":
		answer = question.choice4
	elif question.choice5 != "":
		answer = question.choice5
	return answer

def findAnswerForMC(question):
	if question.isAnswer1 == True:
		answer = "1"
	elif question.isAnswer2 == True:
		answer = "2"
	elif question.isAnswer3 == True:
		answer = "3"
	elif question.isAnswer4 == True:
		answer = "4"
	elif question.isAnswer5 == True:
		answer = "5"
	return answer

def findAnswerForAA(question):
	answerList = []
	if question.isAnswer1 == True:
		answerList.append("1")
	if question.isAnswer2 == True:
		answerList.append("2")
	if question.isAnswer3 == True:
		answerList.append("3")
	if question.isAnswer4 == True:
		answerList.append("4")
	if question.isAnswer5 == True:
		answerList.append("5")
	return answerList


# Helper function for addQuestion and editQuestion
def classifyQuestionType(question):
	isAnswerCounter = 0
	choiceCounter = 0

	question.choice1 = question.choice1.strip()
	if question.choice1 != "":
		choiceCounter += 1
		if question.isAnswer1 == True:
			isAnswerCounter += 1
	else:
		question.isAnswer1 = False
	question.choice2 = question.choice2.strip()
	if question.choice2 != "":
		choiceCounter += 1
		if question.isAnswer2 == True:
			isAnswerCounter += 1
	else:
		question.isAnswer2 = False
	question.choice3 = question.choice3.strip()
	if question.choice3 != "":
		choiceCounter += 1
		if question.isAnswer3 == True:
			isAnswerCounter += 1
	else:
		question.isAnswer3 = False
	question.choice4 = question.choice4.strip()
	if question.choice4 != "":
		choiceCounter += 1
		if question.isAnswer4 == True:
			isAnswerCounter += 1
	else:
		question.isAnswer4 = False
	question.choice5 = question.choice5.strip()		
	if question.choice5 != "":
		choiceCounter += 1
		if question.isAnswer5 == True:
			isAnswerCounter += 1
	else:
		question.isAnswer5 = False
			
	# classify the question type
	if choiceCounter != 0:
		if choiceCounter == 1:
			questionType = SHORT_ANSWER
		else:
			if isAnswerCounter == 1:
				questionType = MULTIPLE_CHOICE
			else:
				questionType = ALL_THAT_APPLY
	else:
		questionType = "Invalid"

	return question, questionType
