from postlabq.models import PostlabQuiz, QuestionType, EqType, BaseQuestion, TextInputQuestion, CalQuestion, Constant, FreeResponse
#from xlsinput import XlsInputField

# Postlab quiz title
usr = PostlabQuiz.objects.create(title='Introductory Laboratory Techniques',
        courseNum='2a',fullScore=-1)
usr = PostlabQuiz.objects.create(title='Observing Chemical Reactions',
        courseNum='2a',fullScore=-1)
usr = PostlabQuiz.objects.create(title='Reactions of Copper',
        courseNum='2a',fullScore=-1)
usr = PostlabQuiz.objects.create(title='Volumetric Analysis II',
        courseNum='2a',fullScore=-1)
usr = PostlabQuiz.objects.create(title='Volumetric Analysis I',
        courseNum='2a',fullScore=-1)
usr = PostlabQuiz.objects.create(title='Spectroscopic Analysis of Mixture',
        courseNum='2a',fullScore=-1)
usr = PostlabQuiz.objects.create(title='Determining Avogadro\'s Number',
        courseNum='2a',fullScore=-1)
#
usr = QuestionType.objects.create(quesType='one_num_input',inpNum=1)
usr = QuestionType.objects.create(quesType='three_num_input',inpNum=3)
usr = QuestionType.objects.create(quesType='varied_num_input',inpNum=-1)
usr = QuestionType.objects.create(quesType='single_choice',inpNum=1)
usr = QuestionType.objects.create(quesType='multiple_choice',inpNum=-1)
usr = QuestionType.objects.create(quesType='constant',inpNum=1)
usr = QuestionType.objects.create(quesType='freeresponse',inpNum=1)
usr = QuestionType.objects.create(quesType='puretext',inpNum=0)
##
eq1 = EqType.objects.create(description='division',inpNum=2,oprtlst='/')
eq2 = EqType.objects.create(description='sub',inpNum=2,oprtlst='-')
eq3 = EqType.objects.create(description='division2',inpNum=3,oprtlst=['/','/'])
eq4 = EqType.objects.create(description='mult-div',inpNum=3,oprtlst=['*','/'])
eq5 = EqType.objects.create(description='mult-sub',inpNum=4,oprtlst=['*','-','*'])
eq6 = EqType.objects.create(description='average',inpNum=2,oprtlst=['ave'])
eq7 = EqType.objects.create(description='standard dev',inpNum=2,oprtlst=['stddev'])
eq8 = EqType.objects.create(description='conf limit',inpNum=2,oprtlst=['conflim'])
eq9 = EqType.objects.create(description='relative err',inpNum=2,oprtlst=['relerr'])
eq10 = EqType.objects.create(description='percentage',inpNum=2,oprtlst=['perctg'])
eq11 = EqType.objects.create(description='mult3-div',inpNum=5,oprtlst=['*','*','*','/'])
eq12 = EqType.objects.create(description='inverse',inpNum=1,oprtlst=['inv'])
eq13 = EqType.objects.create(description='mult2',inpNum=3,oprtlst=['*','*'])
eq14 = EqType.objects.create(description='get_volume',inpNum=1,oprtlst=['volume'])

sch1 = ScoreScheme.objects.create(description='0',scheme=[0])
sch2 = ScoreScheme.objects.create(description='3321',scheme=[3,3,2,1])
sch3 = ScoreScheme.objects.create(description='3221',scheme=[3,2,2,1])
sch4 = ScoreScheme.objects.create(description='3211',scheme=[3,2,1,1])
