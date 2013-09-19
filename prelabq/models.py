from django.db import models
from prelabq.customField import SeparatedValuesField
from django.contrib.auth.models import User

# Create your models here.
class PrelabQuiz(models.Model):
    """class for prelabquiz name"""
    quizName = models.CharField(max_length=255)
    courseNum = models.CharField(max_length=2)
    def __unicode__(self):
       return self.quizName
    # choices3 = SeparatedValuesField()
    #alt = models.CharField(max_length=255)

class QuizItems(models.Model):
    """ questions and all choices and answers"""
    quiz = models.ForeignKey(PrelabQuiz)
    question = models.CharField(max_length=255)
    choices = SeparatedValuesField(token="$")
    answer = models.IntegerField()

    def __unicode__(self):
       return self.question

class UserPrelabScore(models.Model):
    """ total prelab scores for each student"""
    user = models.ForeignKey(User)
    numQuiz = models.IntegerField();
    #quizSc = models.CommaSeparatedIntegerField(max_length=64)
    quizSc = SeparatedValuesField(token=",")

class UserPrelabQuiz(models.Model):
    """ detail information and score for each quiz for each student"""
    user = models.ForeignKey(UserPrelabScore)
    quiztk = models.ForeignKey(PrelabQuiz)
    score1 = models.IntegerField()
    score2 = models.IntegerField()
    scoreadj = models.IntegerField()
