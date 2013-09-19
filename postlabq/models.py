from django.db import models
from prelabq.customField import SeparatedValuesField
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.utils import timezone
import types
import postlabq.utils
import postlabq.eqeval
import re,copy

# Create your models here.
class PostlabQuiz(models.Model): 
    """Postlabquiz title and full credit"""
    title = models.CharField(max_length=255)
    courseNum = models.CharField(max_length=2)
    fullScore = models.IntegerField()
    def __unicode__(self):
       return self.title

class QuestionType(models.Model): 
    """number of input fields for different questions"""
    quesType = models.CharField(max_length=64,unique=True)
    inpNum = models.IntegerField()
    def __unicode__(self):
       return self.quesType

class EqType(models.Model):
    """different kinds of equations for questions"""
    description = models.CharField(max_length=64)
    inpNum = models.IntegerField()
    oprtlst = SeparatedValuesField(token='$')
    def __unicode__(self):
       return self.description

class BaseQuestion(models.Model):
    """base question only has the common fields of all different questions"""
    ques = models.ForeignKey(QuestionType)
    quiz = models.ForeignKey(PostlabQuiz)
    question = models.TextField()
    orderNum = models.CharField(max_length=16,unique=True)
    dispNum = models.CharField(max_length=16)
    part=models.CharField(max_length=8)
    def usrentcreate(self,request,usr,usrAns):
        return None
    def getquesfd(self):
        return self.ques.inpNum
    def getquestp(self):
        return self.ques.quesType
    def __unicode__(self):
       return self.question

class FreeResponse(BaseQuestion):
    """freeresponse questions"""
    fullcredit = models.IntegerField()
    gradeText = SeparatedValuesField(token='$')
    def usrentcreate(self,request,usr,usrAns):
        return usr.userpostlabfree_set.create(
                user=request.user, questk=self,
                response=usrAns, score=-1, pub_time=timezone.now().ctime()
                )
    def __unicode__(self):
       return self.question

class Constant(BaseQuestion):
    """fields for constant values""" 
    value = models.FloatField()
    annotated = models.CharField(max_length=16)
    def usrentcreate(self,request,usr,usrAns):
        return None
    def __unicode__(self):
       return self.annotated

class TextInputQuestion(BaseQuestion):
    """questions for input values"""
    #question = models.CharField(max_length=255)
    answer = models.FloatField()
    tolerance = models.CharField(max_length=64)
    #inputLabel = models.CharField(max_length=64)
    inputLabel = SeparatedValuesField(token='&')
    #scscheme = models.ForeignKey(ScoreScheme)
    scscheme = SeparatedValuesField(token='$')
    gradeText = SeparatedValuesField(token='$')
    fullcredit = models.IntegerField()
    verify = models.BooleanField()
    def usrentcreate(self,request,usr,usrAns):
        return usr.userpostlabbase_set.create(
                user=request.user, questk=self,
                stdanswer=self.getstdans(), fullcredit = self.getcredit(),
                answer=usrAns, score=-1, pub_time=timezone.now().ctime()
                )
    def getstdans(self):
        return [self.answer]
    def getcredit(self):
        return self.fullcredit
    def __unicode__(self):
       return self.inputLabel[0]

class ChoiceQuestion(BaseQuestion):
    """multiple choice question"""
    #question = models.CharField(max_length=255)
    choices = SeparatedValuesField(token="$")
    answer = SeparatedValuesField(token="$")
    gradeText = SeparatedValuesField(token='$')
    #scscheme = models.ForeignKey(ScoreScheme)
    scscheme = SeparatedValuesField(token='$')
    fullcredit = models.IntegerField()
    def usrentcreate(self,request,usr,usrAns):
        return usr.userpostlabbase_set.create(
                user=request.user, questk=self,
                stdanswer=self.getstdans(), fullcredit = self.getcredit(),
                answer=usrAns, score=-1, pub_time=timezone.now().ctime()
                )
    def getstdans(self):
        return [self.answer]
    def getcredit(self):
        return self.fullcredit
    def __unicode__(self):
       return self.question

class CalQuestion(BaseQuestion):
    """questions that need calculations"""
    scscheme = SeparatedValuesField(token='$')
    gradeText = SeparatedValuesField(token='$')
    inp = models.ManyToManyField(BaseQuestion,related_name='calq')
    eq = models.ForeignKey(EqType)
    inputLabel = SeparatedValuesField(token='&')
    tolerance = models.CharField(max_length=64)
    fullcredit = models.IntegerField()
    def usrentcreate(self,request,usr,usrAns):
        return usr.userpostlabbase_set.create(
                user=request.user, questk=self,
                stdanswer=self.getstdans(usr), fullcredit = self.getcredit(),
                answer=usrAns, score=-1, pub_time=timezone.now().ctime()
                )
    def getstdans(self,usr):
        (depqbase,oprtr)=self.getdeplst()
        inp=usr.getdepinput(depqbase)
        stdAns = postlabq.eqeval.evaluate(inp,oprtr)
        print 'stdAns:',stdAns
        if type(stdAns) is types.FloatType:
            stdAns = [stdAns]
        if self.ques.inpNum != len(stdAns):
            raise postlabq.utils.ValidationError("Stdanswer num does not match its question type")
        return stdAns
    def getcredit(self):
        return self.fullcredit
    def getdeplst(self):
        oprtr = self.eq.oprtlst
        print "self:", self.id
        for i in self.inp.through.objects.filter(calquestion=self):
            print i.pk
        depqbase = [i.basequestion for i in
                self.inp.through.objects.filter(calquestion=self).order_by('id')]
        return depqbase,oprtr

    def nextquestion(self):
        pass
    def __unicode__(self):
        return self.question

class UserPostlabScore(models.Model):
    """scores of each postlab for each student """
    user = models.ForeignKey(User)
    quiz = models.ForeignKey(PostlabQuiz)
    baseScore = models.IntegerField()
    freeScore = models.IntegerField()
    presScore = models.IntegerField()
    adjScore = models.IntegerField()
    adjText = SeparatedValuesField(token='$')
    totScore = models.IntegerField()
    pub_time = models.DateTimeField()
    def getdepinput(self,depqbase):
        inp = []
        for qu in depqbase:
            try:
                depq = self.userpostlabbase_set.get(questk_id=qu.id)
                fd = depq.questk.ques.inpNum
                if fd == 1:
                    ans = float(depq.answer[len(depq.answer)-1])
                else:
                    ans = [float(depq.answer[len(depq.answer)-i]) for i in range(fd,0,-1)]
                #ans = depq.answer
            except UserPostlabBase.DoesNotExist:
                depq = Constant.objects.get(id=qu.id)
                fd = depq.ques.inpNum
                ans = depq.value
            inp.append(ans)
        return inp

    def getbaselist(self):
        return UserPostlabBase.objects.filter(user=self.user,quiz=self.postlab)
    def getfreelist(self):
        return UserPostlabFree.objects.filter(user=self.user,quiz=self.postlab)

    def alldelete(self):
        lst = self.getbaselist()
        for q in lst:
            q.qzdelete()
        lst = self.getfreelist()
        for q in lst:
            q.qzdelete()
        self.delete()

    def dispquestion(self,request):
        prevu = self.userpostlabbase_set.filter(user=self.user)
        dispanstime=[]
        for pu in prevu:
            fd = pu.questk.ques.inpNum
            ans = ['  '.join([str(pu.answer[i]) for i in range(p*fd,(p+1)*fd)]) for p in range(len(pu.answer)/fd)]
            print "pub_time:",pu.pub_time
            time = [t for t in pu.pub_time]
            dispanstime.append(zip(ans,time))
        dispques=[qu.questk.question for qu in prevu]
        dispqid=[qu.questk.orderNum for qu in prevu]
        dispq = zip(dispqid, dispques, dispanstime)
        return dispq

    def updatepresscr(self,pts):
        if pts+self.totScore > self.postlab.fullScore or pts > 2:
            return False
        else:
            self.presScore = pts
            self.totScore += pts
            self.save()
            return True

    def updateadjscr(self,pts,text):
        if pts+self.totScore > self.postlab.fullScore:
            return False 
        else:
            self.adjScore=pts
            self.adjText=self.adjText.append(text)
            self.totScore += pts
            self.save()
            return True 

    def updatefreescr(self, score):
        self.freeScore = score
        self.totScore += score
        self.save()
        return True

    def updatebasescr(self, score):
        self.baseScore = score
        self.totScore += score
        self.save()
        return True

    def updatetotscr(self):
        self.totScore=self.presScore+self.baseScore+self.freeScore+self.adjScore
        self.save()
        return True

    def __unicode__(self):
        time = self.pub_time
        return time[len(time)-1].ctime()

class UserPostlabBase(models.Model):
    """details information for each question of the chosen postlab of each
    student"""
    user = models.ForeignKey(User)
    questk = models.ForeignKey(BaseQuestion)
    postlab = models.ForeignKey(UserPostlabScore)
    answer = SeparatedValuesField(token='$')
    stdanswer = SeparatedValuesField(token='$')
    score = models.IntegerField()
    fullcredit = models.IntegerField()
    pub_time = SeparatedValuesField(token='$')

    def updatescore(self):
        return self.postlab.updatebasescr(self.score)

    def getstdanswer(self,q,usr):
        (depqbase,oprtr)=q.getdeplst()
        inp=usr.getdepinput(depqbase)
        stdAns = postlabq.eqeval.evaluate(inp,oprtr)
        print "stdans:",stdAns
        return stdAns

    def chkchance(self):
        anslst = [float(a) for a in self.answer]
        fd = self.questk.ques.inpNum
        chancetk = len(anslst)/fd+1
        if self.score == self.fullcredit:
            return False
        else:
            return True

    def qzdelete(self):
        user = self.user
        quiz = self.postlab
        q = self.qeustk
        if hasattr(q,'calquestion'):
            depq = q.inp
            for ques in depq:
                entry = UserPostlabBase.objects.get(user=user,quiz=quiz,questk=ques)
                entry.delete()
        self.delete()

    def rppresent(self):
        ans = self.answer
        stamp = self.pub_time
        assert len(ans) == len(stamp), "publish time number should match answer list number"
        return zip(ans,stamp),score

    def getmsg(self,q,correct):
        anslst = self.answer
        if correct==False:
            fd = self.questk.ques.inpNum
            idx = len(anslst)/fd
            print idx
            if idx >= len(q.gradeText):
                text = q.gradeText[-1]
            else:
                text =  q.gradeText[idx]
        else:
            text = q.gradeText[0]
        pat = re.findall('(##([0-9]+)##)',text)
        msg = text
        print msg
        if pat != []:
            for fd in pat:
                idx = eval(fd[1])
                try:
                    t=UserPostlabBase.objects.get(user=self.user,questk=self.questk,postlab=self.postlab)
                except UserPostlabBase.DoesNotExist:
                    print "Refer an unexisted userpostlabbase entry which is impossible!"
                ansstr = t.getanswer()
                msg = msg.replace(fd[0],ansstr)
        return msg

    def getanswer(self):
        anslst = self.answer
        fd = self.questk.ques.inpNum
        return ', '.join(anslst[-fd:])

    def saveanswer(self,q,usrAns):
        stdAns = self.stdanswer
        fd = q.ques.inpNum
        assert fd == len(usrAns), "user input fields number does not match that of standard"
        print self.answer
        anslst = [float(a) for a in self.answer]
        print "answer:",anslst
        anslst.extend([float(a) for a in usrAns])
        print "anslst:",anslst
        self.answer = anslst
        self.pub_time.append(timezone.now().ctime())
        self.save()
        return

    def chkanswer(self,q,usrAns):
        stdAns = self.stdanswer
        fd = q.ques.inpNum
        assert fd == len(usrAns), "user input fields number does not match that of standard"
        if isinstance(q,ChoiceQuestion):
            for u,s in zip(usrAns, stdAns):
                if float(u) != float(s):
                    return False
        else:
            tol = q.tolerance
            print "tol:",tol
            if '$' not in tol:
                tp=1
                toll=tolu=float(tol)
            else:
                tp=0
                if isinstance(q,TextInputQuestion):
                    tp=2
                [toll,tolu]=[float(t) for t in tol.split('$')]
            print "usrans",usrAns
            print "stdans",stdAns
            print "tp:",tp
            print "toll,tolu:",toll,tolu
            if tp == 0:
                for u,s in zip(usrAns, stdAns):
                    print u
                    print s
                    if float(u) < float(s)*toll or float(u) > float(s)*tolu:
                        return False
            elif tp == 1:
                for u,s in zip(usrAns, stdAns):
                    print "u:",u
                    print "s:",s
                    if float(u) < float(s)-toll or float(u) > float(s)+tolu:
                        return False
            elif tp == 2:
                for u in usrAns:
                    if float(u)<toll or float(u) >tolu:
                        return False
        scoresch = q.scscheme
        chancetot = len(scoresch)
        chancetk = len(self.answer)/fd
        if chancetk > chancetot:
            self.score = 0
        else:
            self.score = eval(scoresch[chancetk-1])
        self.save()
        return True

    def __unicode__(self):
        time = self.pub_time
        return time[len(time)-1]

class UserPostlabFree(models.Model):
    """details information for free reponses for chosen postlab and each
    student"""
    user = models.ForeignKey(User)
    questk = models.ForeignKey(FreeResponse)
    postlab = models.ForeignKey(UserPostlabScore)
    response = models.TextField()
    score = models.IntegerField()
    pub_time = models.DateTimeField()

    def updatescore(self):
        return self.postlab.updatefreescr(self.score)

    def addscore(self,pts):
        fullcredit=self.questk.fullcredit
        if pts>fullcredit:
            return -1
        else:
            self.score=pts
            self.save()
            return 0
        
    def qzdelete(self):
        self.delete()

    def __unicode__(self):
        time = self.pub_time.ctime()
        return time[len(time)-1].ctime()
