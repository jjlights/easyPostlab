#from postlabq.models import PostlabQuiz, QuestionType, EqType, BaseQuestion, Constant, TextInputQuestion, CalQuestion, ChoiceQuestion, FreeResponse, SubQuiz, UserPostlabBase, UserPostlabFree, UserPostlabScore

class ValidationError(Exception):
    def __init__(self, message):
        self.message = message

def spcquestion(ques):
    if hasattr(ques, 'textinputquestion'):
        return ques.textinputquestion
    elif hasattr(ques, 'calquestion'):
        return ques.calquestion
    elif hasattr(ques, 'choicequestion'):
        return ques.choicequestion
    elif hasattr(ques, 'constant'):
        return ques.constant
    elif hasattr(ques, 'freeresponse'):
        return ques.freeresponse
    else:
        return ques

