import os
from random import randint

def populate():
    user1 = User(username='udacian', password='1234')

    for i in range(1, 11):
        cardSet = CardSet.objects.get_or_create(name='cardset' + str(i), user=user1, isPublic=True)[0]
        for j in range(1, 21):
            questionType = j % 3
            if questionType == 0:
                questionType = "Short Answer"
            elif questionType == 1:
                questionType = "Multiple Choice"
            else:
                questionType = "All that Apply"
            question = Question.objects.get_or_create(question='question' + str(j),
                                questionType=questionType,
                                cardSet=cardSet)
            if questionType == 0:
                choice = Choice.objects.get_or_create(choice="Answer", isAnswer=True, question=question)[0]
            elif questionType == 1:
                numberOfChoice = randint(2,6)
                answer = randint(1,numberOfChoice + 1)
                for k in range(1,numberOfChoice + 1):
                    if k == answer:
                        choice = Choice.objects.get_or_create(choice="choice" + str(k), isAnswer=True, question=question)[0]
                    else:
                        choice = Choice.objects.get_or_create(choice="choice" + str(k), isAnswer=False, question=question)[0]
            else:
                for k in range(1,6):
                    if k == 1 or k == 3 or k == 5:
                        choice = Choice.objects.get_or_create(choice="choice" + str(k), isAnswer=True, question=question)[0]
                    else:
                        choice = Choice.objects.get_or_create(choice="choice" + str(k), isAnswer=False, question=question)[0]

    print "Done"

# Start execution here!
if __name__ == '__main__':
    print "Starting Flash population script..."
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'flashcard.settings')
    from django.contrib.auth.models import User
    from flash.models import CardSet, Question, Choice
    print "working"
    populate()


