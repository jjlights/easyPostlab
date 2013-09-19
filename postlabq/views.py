from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User, Group, Permission
from django import forms
from django.utils import timezone
from postlabq.models import PostlabQuiz, QuestionType, EqType, BaseQuestion, Constant, TextInputQuestion, CalQuestion, ChoiceQuestion, FreeResponse, SubQuiz, UserPostlabBase, UserPostlabFree, UserPostlabScore
from postlabq.postlabpage import PostlabDisplay, PostlabForm
import postlabq.eqeval
import postlabq.utils
import random
import datetime, types

csnum=u'2a'
numQuiz=8
numQuestion=3

numfd = {
        'one_num_input':1,
        'three_num_input':3,
        'single_choice':1,
        'multiple_choice':1,
        }

def getanswer(questp,keys,request):
    usrAns = []
    if questp == 'one_num_input':
        usrAns = [request.POST.get(keys[0])]
    elif questp == 'three_num_input':
        usrAns = [request.POST.get(key) for key in keys]
    elif questp == 'single_choice':
        usrAns = [request.POST.get(keys[0])]
    elif questp == 'multiple_choice':
        usrAns = [request.POST.get(keys[0])]
    return usrAns

def choiceItem(question):
    return [(idx, q) for idx, q in enumerate(question.choices)]

def chooseQuestion(quiz_id, *args, **kwargs):
    default = numQuestion
    numQ = kwargs.pop('numQuestion',default)
    qlist = QuizItems.objects.filter(quiz_id=quiz_id)
    return random.sample(qlist, numQ)

def postlablst(request):
    if request.user.is_authenticated():
        lst = PostlabQuiz.objects.filter(courseNum__in=[csnum]).order_by('id')
        user_perms = list(request.user.get_all_permissions())
        userid = request.user.id
        if user_perms == [unicode('auth.can_view')]:
            return render_to_response('postlabq/postlablst.html',
                    {'lst':lst, 'type':0,},
                    context_instance=RequestContext(request))
        else:
            return render_to_response('postlabq/postlablst.html',
                    {'lst':lst, 'type':1,},
                    context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/login/')

def postlabqz(request,quiz_id):
    if request.user.is_authenticated():
        quiz = PostlabQuiz.objects.get(id=quiz_id)
        queslst = BaseQuestion.objects.filter(quiz=quiz,orderNum__startswith='q')
        if request.method == 'POST':
            form = PostlabForm(request.POST)
            keys=request.POST.keys()
            keys = [k for k in keys if k != u'csrfmiddlewaretoken']
            print "keys:",keys
            print len(keys)
            if len(keys)==1 and not keys[0].startswith('8'):
                assert request.POST[keys[0]]!='',"Input field could not be empty"

            qid = int(str(keys[0]).split('-')[1])
            qbase = BaseQuestion.objects.get(id=qid)
            q=postlabq.utils.spcquestion(qbase)

            usrAns = getanswer(q.getquestp(),keys,request)
            fd = q.getquesfd()
            print fd
            print q.getquestp()
            print len(usrAns)
            if fd == -1:
                if isinstance(q,ChoiceQuestion):
                    fd=len(q.answer)
            assert len(usrAns) == fd, 'User answer fields does not match question type'
            print usrAns
            try:
                usr = UserPostlabScore.objects.get(user=request.user,quiz_id=quiz_id)
            except UserPostlabScore.DoesNotExist:
                usr = UserPostlabScore.objects.create(user=request.user,quiz_id=quiz_id,
                        presScore=0,freeScore=0,baseScore=0,adjScore=0,adjText=[''],
                        totScore=-1,pub_time=timezone.now()
                        )
            try:
                u = usr.userpostlabbase_set.get(user=request.user,questk_id=q.id)
            except UserPostlabBase.DoesNotExist:
                u = q.usrentcreate(request,usr,usrAns)
                if u==None:
                    dispq=usr.dispquestion(request)
                    nextq = 'q'+str(int(q.orderNum[1:])+1).zfill(3)
                    print nextq
                    ques = BaseQuestion.objects.get(orderNum=nextq)
                    q=postlabq.utils.spcquestion(ques)
                    tp = 1
                    form = PostlabForm(question=q)
                    message='Continue...'
                    return render_to_response('postlabq/postlabqz.html',
                            {'quiz_id':quiz_id, 'question':(q.orderNum[1:],q.question),
                                'form':form, 'dispq':dispq,'message':message,'tp':tp},
                        context_instance=RequestContext(request))
            else:
                if not u.chkchance():
                    message = 'You have already finished this question, goto the next one...'
                    dispq=usr.dispquestion(request)
                    return render_to_response('postlabq/postlabqz.html',
                            {'quiz_id':quiz_id, 'question':(q.orderNum[1:],q.question),
                        'form':form, 'dispq':dispq, 'message':message},
                    context_instance=RequestContext(request))
                u.saveanswer(q,usrAns)
            if isinstance(q,TextInputQuestion) and q.verify == 0:
                nextq = 'q'+str(int(q.orderNum[1:])+1).zfill(3)
                ques = BaseQuestion.objects.get(orderNum=nextq)
                message = u.getmsg(q,True)
                q=postlabq.utils.spcquestion(ques)
            else:
                if u.chkanswer(q,usrAns):
                    message = u.getmsg(q,True)
                    nextq = 'q'+str(int(q.orderNum[1:])+1).zfill(3)
                    ques = BaseQuestion.objects.get(orderNum=nextq)
                    q=postlabq.utils.spcquestion(ques)
                else:
                    message = u.getmsg(q,False)
            form = PostlabForm(question=q)
            dispq=usr.dispquestion(request)
            print dispq
            return render_to_response('postlabq/postlabqz.html',
                    {'quiz_id':quiz_id, 'question':(q.orderNum[1:],q.question),
                    'form':form, 'dispq':dispq, 'message':message},
                context_instance=RequestContext(request))
        else:
            print queslst
            try:
                usr = UserPostlabScore.objects.get(user=request.user,quiz_id=quiz_id)
            except UserPostlabScore.DoesNotExist:
                ques=queslst[0]
                q=postlabq.utils.spcquestion(ques)
                form = PostlabForm(question=q)
                message='Now work on the first question of the postlab...'
                print "q:", ques
                tp=1
                return render_to_response('postlabq/postlabqz.html',
                        {'quiz_id':quiz_id, 'question':(q.orderNum[1:],q.question),
                            'form':form, 'dispq':[],'message':message,'tp':tp},
                    context_instance=RequestContext(request))
            prevq = usr.userpostlabbase_set.filter(user=request.user)
            print len(prevq)
            idx=len(prevq)-1
            lastprevidx = prevq[idx].questk.orderNum[1:]
            i=len(queslst)-1
            lastques = queslst[i].orderNum[1:]
            while (i>=0):
                if queslst[i].ques.quesType != 'puretext':
                    lastquesidx = queslst[i].orderNum[1:]
                    break
                else:
                    i -= 1
            if lastprevidx<lastquesidx:
                nextq = 'q'+str(int(lastprevidx)+1).zfill(3)
                ques = BaseQuestion.objects.get(orderNum=nextq)
                q=postlabq.utils.spcquestion(ques)
                tp = 1
                form = PostlabForm(question=q)
                dispq=usr.dispquestion(request)
                message='Now work on the question you have left last time...'
                return render_to_response('postlabq/postlabqz.html',
                        {'quiz_id':quiz_id, 'question':(q.orderNum[1:],q.question),
                            'form':form, 'dispq':dispq,'message':message,'tp':tp},
                    context_instance=RequestContext(request))
            elif lastprevidx==lastquesidx:
                form = PostlabForm()
                message='You have already finished this postlab.'
                return render_to_response('postlabq/postlabqz.html',
                    {'quiz_id':quiz_id,'message':message,},
                    context_instance=RequestContext(request))
            else:
                return HttpResponseRedirect('/postlab_quiz/')
    else:
        return HttpResponseRedirect('/postlab_quiz/')
