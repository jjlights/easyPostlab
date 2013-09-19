#display the prelab question pages 
# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User, Group, Permission
from django import forms
from prelabq.models import PrelabQuiz, QuizItems, UserPrelabScore, UserPrelabQuiz
from prelabq.prelabform import PrelabForm
import random

csnum=u'2a'
numQuiz=8
numQuestion=3


def choiceItem(question):
    return [(idx, q) for idx, q in enumerate(question.choices)]

def chooseQuestion(quiz_id, *args, **kwargs): # return the questions list
    default = numQuestion
    numQ = kwargs.pop('numQuestion',default)
    qlist = QuizItems.objects.filter(quiz_id=quiz_id)
    return random.sample(qlist, numQ) 

def prelablst(request):
    if request.user.is_authenticated(): # only authenticated users can see the list
        #csnum = u'2a'
        #lst = [str(q.quizName) for q in PrelabQuiz.objects.filter(courseNum=csnum or u'').order_by('id')]
        lst = PrelabQuiz.objects.filter(courseNum__in=[csnum, u'']).order_by('id')
        user_perms = list(request.user.get_all_permissions())
        userid = request.user.id
        if user_perms == [unicode('auth.can_view')]:
            return render_to_response('prelabq/prelablst.html',
                    {'lst':lst, 'type':0,},
                    context_instance=RequestContext(request))
        else:
            try:
                u = UserPrelabScore.objects.get(user_id=userid)
            except UserPrelabScore.DoesNotExist:
                u = UserPrelabScore.objects.create(user_id=userid,numQuiz=numQuiz,quizSc=[-1]*numQuiz)
            #score = eval(str(u.quizSc))
            score = u.quizSc
            print "score:", score
            safety_qz = int(score[0])
            if safety_qz == -1:
                return render_to_response('prelabq/prelablst.html',
                        {'lst':lst, 'type':1,},
                        context_instance=RequestContext(request))
            else:
                return render_to_response('prelabq/prelablst.html',
                        {'lst':lst, 'type':2,},
                        context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/login/')

def prelabqz(request,quiz_id):
    if request.user.is_authenticated():
        if request.method == 'POST':
            try:
                userid = UserPrelabScore.objects.get(user_id=request.user.id).id
            except UserPrelabScore.DoesNotExist:
                return HttpResponseRedirect(reverse('prelab_quiz', args=(quiz_id,)))
            try:
                u = UserPrelabQuiz.objects.get(user_id=userid,quiztk_id=quiz_id)
            except UserPrelabQuiz.DoesNotExist:
                u = UserPrelabQuiz.objects.create(user_id=userid,quiztk_id=quiz_id,score1=-1,score2=-1,scoreadj=0)
            if u.score2 != -1 or u.score1 == 2:
                tp = 3
                return render_to_response(
                        'prelabq/prelabres.html',
                        {'type':tp, 'correct':0,'total':0, 'quiz_id':quiz_id},
                        context_instance=RequestContext(request)
                        )

            idlst = request.POST.keys()
            idlst = [i for i in idlst if i != u'csrfmiddlewaretoken']
            print request.POST.items()
            print "idlst:", idlst
            if len(idlst) != numQuestion:
#                return HttpResponseRedirect(reverse('prelab_quiz', args=(int(quiz_id),)))
                return render_to_response(
                        'prelabq/prelabqz.html',
                        {'qchoose': qchoose, 'form':form, 'quiz_id':quiz_id},
                        context_instance=RequestContext(request)
                        )
            qchoose = [QuizItems.objects.get(id=int(q)) for q in idlst if q != u'csrfmiddlewaretoken']
            print qchoose
            form = PrelabForm(qchoose, data=request.POST)
            print "items:",form.fields.items()
            if form.is_valid():
                keys = form.fields.keys()
                print keys
                #usrAns = [int(form.fields.get(k)) for k in keys]
                usrAns = [int(request.POST.get(k)) for k in idlst]
                print usrAns
                #cleaned = form.cleaned_data
                #ans = [cleaned[a] for a in cleaned.keys()]
                stdAns = [q.answer for q in qchoose]
                check = [1 if a==b else 0 for (a,b) in zip(usrAns,stdAns)]
                print "usrans:", usrAns
                print "stdans:", stdAns
                print "check:", check
                correct = sum(check)
                total = len(check)
                if u.score1 == -1:
                    if correct == total:
                        u.score1 = 2
                        tot = UserPrelabScore.objects.get(id=userid)
                        lst = PrelabQuiz.objects.filter(courseNum__in=[csnum, u'']).order_by('id')
                        idx = [qid.id for qid in lst].index(int(quiz_id))
                        tot.quizSc[idx] = unicode(u.score1)
                        tot.save()
                        tp = 0
                    else:
                        u.score1 = 0
                        tp = 1
                    u.save()
                elif u.score2 == -1:
                    if correct == total:
                        u.score2 = 2
                        tp = 0
                    else:
                        u.score2 = 0
                        tp = 2
                    u.save()
                    tot = UserPrelabScore.objects.get(id=userid)
                    lst = PrelabQuiz.objects.filter(courseNum__in=[csnum, u'']).order_by('id')
                    idx = [qid.id for qid in lst].index(int(quiz_id))
                    tot.quizSc[idx] = unicode(u.score2)
                    tot.save()
                return render_to_response(
                        'prelabq/prelabres.html',
                        {'type':tp, 'correct':correct,'total':total, 'quiz_id':quiz_id},
                        context_instance=RequestContext(request)
                        )

            else:
                return render_to_response(
                        'prelabq/prelabqz.html',
                        {'form':form, 'quiz_id':quiz_id},
                        context_instance=RequestContext(request)
                        )
        else:
            try:
                userid = UserPrelabScore.objects.get(user_id=request.user.id).id
            except UserPrelabScore.DoesNotExist:
                return HttpResponseRedirect(reverse('/prelab_quiz/', args=(quiz_id,)))
            try:
                u = UserPrelabQuiz.objects.get(user_id=userid,quiztk_id=quiz_id)
            except UserPrelabQuiz.DoesNotExist:
                u = UserPrelabQuiz.objects.create(user_id=userid,quiztk_id=quiz_id,score1=-1,score2=-1,scoreadj=0)
            if u.score2 != -1 or u.score1 == 2:
                tp = 3
                return render_to_response(
                        'prelabq/prelabres.html',
                        {'type':tp, 'correct':0,'total':0, 'quiz_id':quiz_id},
                        context_instance=RequestContext(request)
                        )

            qchoose = chooseQuestion(quiz_id)
            form = PrelabForm(qchoose,initial=dict([(str(q.id),'0') for q in qchoose]))
            #form = PrelabForm(qchoose)
            print "form:", form
            print form.fields.items()
            return render_to_response(
                    'prelabq/prelabqz.html',
                    {'qchoose': qchoose, 'form':form, 'quiz_id':quiz_id},
                    context_instance=RequestContext(request)
                    )
    else:
        return HttpResponseRedirect('/login/')
