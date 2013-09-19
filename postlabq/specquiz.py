from postlabq.models import PostlabQuiz, QuestionType, EqType, BaseQuestion, TextInputQuestion, ChoiceQuestion, CalQuestion, Constant, FreeResponse, UserPostlabBase, UserPostlabFree, UserPostlabScore
from postlabq.xlsinput import XlsInputField
from django.db import IntegrityError
from django.db.models import Max
import types

def retinp(xlsinp,quiz,inpfd,oprtr):
    inp=[]
    for fd in inpfd:
        if type(fd) == types.StringType:
            print fd
            value = float(fd[1:])
            try:
                cons = Constant.objects.get(value=value,quiz=quiz)
            except Constant.DoesNotExist:
                ind = Constant.objects.count()+1
                cons = Constant.objects.create(quiz=quiz,orderNum='c'+str(ind).zfill(2),
                        part='',ques_id=6,question='',dispNum='', value=value,annotated='')
            inp.append(cons)
        elif xlsinp.qlabel.get(fd,-1) == -1:
            print fd
            assert xlsinp.qchoice.get(fd,-1) != -1, "Must be either choice or text question"
            inp.append(ChoiceQuestion.objects.get(quiz=quiz,orderNum='q'+str(fd-indf+1).zfill(3)))
        elif xlsinp.verifyeq(fd) == False:
            inp.append(TextInputQuestion.objects.get(quiz=quiz,orderNum='q'+str(fd-indf+1).zfill(3)))
        else:
            inp.append(CalQuestion.objects.get(quiz=quiz,orderNum='q'+str(fd-indf+1).zfill(3)))

    eqlst = EqType.objects.all()
    for eq in eqlst:
        if oprtr == eq.oprtlst:
            break
    else:
        print oprtr
        EqType.objects.create(description='',inpNum=len(inpfd),oprtlst=oprtr)
    return inp

def DBBuild(flname): 
    xlsinp = XlsInputField(flname)
    
    quiz = PostlabQuiz.objects.get(title__regex=r'^Spectro')
    
    find1=False
    indf=-1
    indl=-1
    for ind,s in xlsinp.qtext.items():
        if s!='' and not find1:
            indf=ind
            find1=True
            continue
        elif s=='' and find1:
            indl=ind
            break
    
    assert indf != -1, "No Text in Question Field!"
    if indl == -1:
        indl = ind
    
    print "indf:%d, indl:%d" %(indf,indl)
    UserPostlabBase.objects.get(quiz=quiz).delete()
    UserPostlabFree.objects.get(quiz=quiz).delete()
    UserPostlabScore.objects.get(quiz=quiz).delete()
    FreeResponse.objects.get(quiz=quiz).delete()
    ChoiceQuestion.objects.get(quiz=quiz).delete()
    CalQuestion.objects.get(quiz=quiz).delete()
    TextInputQuestion.objects.get(quiz=quiz).delete()
    BaseQuestion.objects.get(quiz=quiz).delete()
    
    for ind in range(indf,indl+1):
        fullcredit = 0
        if xlsinp.scorescheme[ind][0] != '':
            fullcredit = eval(xlsinp.scorescheme[ind][0])
        if xlsinp.qfree.get(ind,-1) == -1:
            if xlsinp.qlabel.get(ind,-1) == -1:
                if xlsinp.qchoice.get(ind,-1) == -1:  # Then must be an intermittent base question  
                    questp = QuestionType.objects.get(quesType='puretext')
                    try:
                        BaseQuestion.objects.create(quiz=quiz,ques=questp,question=xlsinp.qtext[ind],orderNum='q'+str(ind-indf+1).zfill(3),
                            dispNum=xlsinp.questionNum[ind]+xlsinp.moduleNum[ind],part=xlsinp.questionNum[ind])
                    except IntegrityError:
                        pass
                else:  # Must be a choice question
                    questype = 'single_choice'
                    if len(xlsinp.newanswer[ind]) > 1:
                        questype = 'multiple_choice'
                    questp = QuestionType.objects.get(quesType=questype)
                    try:
                        ChoiceQuestion.objects.create(quiz=quiz,ques=questp,question=xlsinp.qtext[ind],orderNum='q'+str(ind-indf+1).zfill(3),
                             dispNum=xlsinp.questionNum[ind]+xlsinp.moduleNum[ind],part=xlsinp.questionNum[ind],
                             choices=xlsinp.qchoice[ind],answer=xlsinp.newanswer[ind],
                             gradeText=xlsinp.gradetext[ind],scscheme=xlsinp.scorescheme[ind],fullcredit=fullcredit)
                    except IntegrityError:
                        pass
            else:
                if xlsinp.verifyeq(ind) == False: # TextInputQuestion
    
                    verify=False
                    if xlsinp.verify[ind] in ['y','Y']:
                        verify=True
                    (toll,tolu)=xlsinp.gettol(ind)
                    if toll==None:
                        tol=''
                    elif toll == tolu:
                        tol = str(toll)
                    else:
                        tol = str(toll)+'$'+str(tolu)
                    questp = xlsinp.getquestp(ind)
                    ques = QuestionType.objects.get(quesType=questp)
                    try:   
                        TextInputQuestion.objects.create(quiz=quiz,question=xlsinp.qtext[ind],orderNum='q'+str(ind-indf+1).zfill(3),
                            dispNum=xlsinp.questionNum[ind]+xlsinp.moduleNum[ind],part=xlsinp.questionNum[ind],
                            answer=0.0,tolerance=tol,ques=ques,verify=verify,
                            inputLabel=xlsinp.qlabel[ind],gradeText=xlsinp.gradetext[ind],
                            scscheme=xlsinp.scorescheme[ind],fullcredit=fullcredit)
                    except IntegrityError:
                        pass
                else:
                    (toll,tolu)=xlsinp.gettol(ind)
                    if toll==None:
                        tol=''
                    elif toll == tolu:
                        tol = str(toll)
                    else:
                        tol = str(toll)+'$'+str(tolu)
                    (inpfd,oprtr)=xlsinp.eqdep(ind)
                    assert inpfd != None,"Must return dependent inpfd!"
                    print inpfd,oprtr,ind
                    inp = retinp(xlsinp,quiz,inpfd,oprtr)
                    eqfd=EqType.objects.get(oprtlst=oprtr)
                    questp = xlsinp.getquestp(ind)
                    questp = QuestionType.objects.get(quesType=questp)
                    try:
                        cal=CalQuestion.objects.create(quiz=quiz,question=xlsinp.qtext[ind],orderNum='q'+str(ind-indf+1).zfill(3),
                           dispNum=xlsinp.questionNum[ind]+xlsinp.moduleNum[ind],part=xlsinp.questionNum[ind],
                           tolerance=tol,eq=eqfd,ques=questp,
                           inputLabel=xlsinp.qlabel[ind],gradeText=xlsinp.gradetext[ind],
                           scscheme=xlsinp.scorescheme[ind],fullcredit=fullcredit)
                        for fd in inp:
                            cal.inp.add(fd)
                        cal.save()
                    except IntegrityError:
                        pass
        else: # must be a free response question
            questp = QuestionType.objects.get(quesType='freeresponse')
            try:
                FreeResponse.objects.create(quiz=quiz,ques=questp,question=xlsinp.qfree[ind],orderNum='q'+str(ind-indf+1).zfill(3),
                    dispNum=xlsinp.questionNum[ind]+xlsinp.moduleNum[ind],part=xlsinp.questionNum[ind],
                    gradeText=xlsinp.gradetext[ind],fullcredit=fullcredit)
            except IntegrityError:
                pass

def main():
    flname='PATH/TO/XLSFILE' 
    DBBuild(flname)

if __name__ == "__main__":
    main()
