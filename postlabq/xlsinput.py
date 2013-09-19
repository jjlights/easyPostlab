from xlrd import open_workbook
import types, re

choice2int = {
        'a':0,
        'b':1,
        'c':2,
        'd':3,
        'e':4,
        'f':5,
        }
def tostr(lst):
    s = ''
    for ele in lst:
        s += ele
    return s

class XlsInputField():
    def getgradetext(self,gradetext):
        newgradetext=[]
        for idx in range(len(gradetext)):
            newtexts = []
            texts = gradetext[idx]
            #idensym = 'input'+self.part[idx]+self.questionNum[idx]+self.moduleNum[idx]
            for text in texts:
                textsplit=text
                pat = re.findall('("Display )?(input *)([0-9a-zA-Z]+)("?)',text)
                if pat!=[]:
                    for fd in pat:
                        ind=self.findind(fd[2],idx)
                        textsplit = textsplit.replace(''.join(fd),'##'+str(ind)+'##')
                    #print textsplit
                newtexts.append(textsplit)
            newgradetext.append(newtexts)
        return newgradetext

    def __init__(self,flname):
        wb = open_workbook(flname)
        name = wb.sheet_names()
        s=wb.sheet_by_name(name[0])
        content = []
        self.part = []
        self.questionNum = []
        self.moduleNum = []
        self.question = []
        self.verify = []
        self.eqtext = []
        self.answer = []
        #self.gradetext = []
        gradetext = []
        self.scorescheme = []
        self.comment = []
# Specific fields of question
        self.qfree = {} # free response question
        self.qtext = {} # actual question
        self.qlabel = {} # label field
        self.qchoice = {} # choice fields
        self.newanswer = {} # store only the answer for multiple choices, need to sourcing other way to put in the answer or equationfor textinputq and calq
        for row in range(s.nrows):
            rowvals = []
            for col in range(s.ncols):
                #val = str(s.cell(row,col).value)
                val = s.cell(row,col).value
                if col==2 or col == 1:
                    try:
                        val = str(int(val))
                    except ValueError:
                        pass
                if type(val) != types.StringType and type(val) != types.UnicodeType:
                    val = str(val).strip()
                rowvals.append(val)
        
            assert len(rowvals)==s.ncols,"column number does not match"
            content.append(rowvals)    
            self.part.append(rowvals[0])
            self.questionNum.append(rowvals[1])
            self.moduleNum.append(rowvals[2])
            self.question.append(rowvals[3])
            self.verify.append(rowvals[4])
            self.eqtext.append(rowvals[5])
            self.answer.append(rowvals[6])
            gradetext.append([rowvals[7],rowvals[9],rowvals[11],rowvals[13]])
            self.scorescheme.append([rowvals[8],rowvals[10],rowvals[12],rowvals[14]])
            #self.comment.append(rowvals[15])

        self.gradetext=self.getgradetext(gradetext)
        assert len(content)==s.nrows,"row number does not match"
        for qindex,ques in enumerate(self.question):
            ind=ques.find('Free Response')
            if ind != -1:
                self.qfree[qindex]=ques
                continue
            assert ques.count('?') <= 1, "More than one question mark has not been supported"
            pat = re.search('a\).*b\).*c\).*d\)',ques)  #choices pattern
            if pat==None:
                #print ques
                m = re.search('e\.* *g\.* *(?:[0-9]+\.*[0-9]+%* *g*m*L*\.* *o*r* *){1,}',ques)  # deal with inconsistency of e.g. string
                if m==None:
                    qtmp = ques.split('.')
                    last=len(qtmp)-1
                    qlast = qtmp[last]
                    indq = qlast.find('?')
                    if indq == -1:
                        self.qtext[qindex]=tostr(qtmp[:last])
                    else:
                        self.qtext[qindex]=tostr(qtmp[:last])+qlast[:indq+1]
                        qlast = qlast[indq+1:]
                else:
                    spl = m.group(0)
                    qtmp = ques.split(spl)
                    pat = re.search('[0-9%(.,] *([a-zA-Z ]+=) *_+ *([a-zA-z]*%*/*[a-zA-Z]*) *\([a-zA-Z0-9]+\)*',qtmp[0]) # extract the fill out pattern
                    if pat != None:
                        qfield = qtmp[0].split(pat.group(0))
                        self.qtext[qindex]=qfield[0]+spl
                        label = pat.grou(1)
                        unit = pat.group(2)
                        assert label != None, "Have not catch the label!"
                        assert unit != None, "Have not catch the unit!"
                        self.qlabel[qindex]=[label,unit]
                        continue
                    else:
                        self.qtext[qindex]=qtmp[0]+spl
                        qlast = qtmp[1]

                pat = re.search('[ (]*([a-zA-Z ]+=) *_+ *([a-zA-z]*%*/*[a-zA-z]*)',qlast) # extract the fill out pattern
                if pat == None:
                    pass
                else:
                    label = pat.group(1)
                    unit = pat.group(2)
                    assert label != None, "Have not catch the label!"
                    assert unit != None, "Have not catch the unit!"
                    self.qlabel[qindex]=[label,unit]
            else:
                sp = pat.group(0)
                qtmp = ques.split(sp)
                #qfield=qtmp[0].split('.')[:2]
                qfield=qtmp[0].split('.')
                self.qtext[qindex]=tostr(qfield)
                    
                inda = sp.find('a)')
                indb = sp.find('b)')
                indc = sp.find('c)')
                indd = sp.find('d)')
                inde = qtmp[1].find('e)')
                if inde == -1:
                    self.qchoice[qindex]=[sp[inda:indb],sp[indb:indc],sp[indc:indd],sp[indd:]+qtmp[1]]
                else:
                    self.qchoice[qindex]=[sp[inda:indb],sp[indb:indc],sp[indc:indd],sp[indd:]+qtmp[1][:inde],qtmp[1][inde:]]
                ans=self.answer[qindex]
                m=re.search('([a-zA-Z]) *a*n*d* *([a-zA-Z]*)',ans)
                assert m != None, "Must have an answer for multiple choices"
                if m.group(2) == None or m.group(2)=='':
                    self.newanswer[qindex]=[choice2int[m.group(1)]]
                else:
                    self.newanswer[qindex]=[choice2int[m.group(1)],choice2int[m.group(2)]]

        return                        
    
    def verifyeq(self,ind):
        text=self.eqtext[ind]
        if text == 'NA' or text=='':
            return False
        else:
            return True

    def eqdep(self, ind):
        oprtr=[]
        inpfd=[]
        text = self.eqtext[ind]
        if text == 'NA' or text == '':
            return (None,'')
        else:
            pat = re.search('([a-zA-Z0-9]+) *= *(.*)',text)
            assert pat != None, "Unsupported format for equation"
            outputf = pat.group(1).lower()
            inputf = pat.group(2).lower()
            idensym = (self.part[ind]+self.questionNum[ind]+self.moduleNum[ind]).lower()
            print "outputf,inputf,idensym:",outputf,inputf,idensym
            #if outputf == 'output'+idensym or 'inputoutput'+idensym in outputf:
            if 'output'+idensym in outputf or 'inputoutput'+idensym in outputf:
                quesinp = 'one_num_input'
            else:
                #assert outputf == 'output'+idensym+'n',"Unsupported string format for output"
                assert 'output'+idensym+'n' in outputf or 'inputoutput'+idensym+'n' in outputf,"Unsupported string format for output"
                quesinp = 'three_num_input'

            pat = re.search(' *([0-9.]+)\*(input[0-9a-zA-Z]+)/sqrt\(([0-9])\)',inputf)
            if pat != None:
                inpstr=pat.group(2)
                numsp=pat.group(3)
                idsymtg=inpstr[5:] if inpstr[-1] != 'n' else inpstr[5:-1]
                indtg = self.findind(idsymtg,ind)
                inpfd.append(indtg)
                inpfd.append('c'+str(numsp))
                print "inpstr:",inpstr
                oprtr.append('conflim')
                return (inpfd,oprtr)
            pat = re.search(' *1\.*0* */ *(input[0-9a-zA-Z]+)',inputf)
            if pat != None:
                inpstr=pat.group(1)
                idsymtg=inpstr[5:]
                indtg = self.findind(idsymtg,ind)
                oprtr.append('inv')
                inpfd.append(indtg)
                return (inpfd,oprtr)
            pat = re.search('^ *\((.*)\)/([0-9])',inputf)
            if pat != None:
                inpstr = pat.group(1)
                num = eval(pat.group(2))
                inpstr=[t.strip() for t in inpstr.split('+')]
                assert len(inpstr) == num, "only mean value is supported"
                idsymtg = inpstr[0][5:-1]
                indtg1 = self.findind(idsymtg,ind)
                oprtr.append('ave')
                inpfd.append(indtg1)
                return (inpfd,oprtr)
            pat = re.search(' *sqrt\(\((.*)\)/([0-9])\) *',inputf)
            if pat != None:
                inpstr = pat.group(1)
                num = eval(pat.group(2))
                inpstr=inpstr.split('+')
                assert len(inpstr) == num+1, "only stddev value is supported"
                pat = re.search(' *\((input[0-9a-zA-Z]+) *- *(input[0-9a-zA-Z]+)\)\^2',inpstr[0])
                assert pat != None, "Format is not supported"
                idsymtg = pat.group(1)[5:-1]
                indtg1 = self.findind(idsymtg,ind)
                idsymtg = pat.group(2)[5:]
                indtg2 = self.findind(idsymtg,ind)
                oprtr.append('stddev')
                inpfd.append(indtg1)
                return (inpfd,oprtr)
            pat = re.search(' *100\*ABS\((input[0-9a-zA-Z]+) *- *(input[0-9a-zA-Z]+)\)/ *(input[0-9a-zA-Z]+)',inputf)
            if pat != None:
                fd1 = pat.group(1)
                fd2 = pat.group(2)
                fd3 = pat.group(3)
                if fd1==fd3:
                    sample = fd2
                    ref = fd1
                else:
                    assert fd2==fd3, "Unsupported Format"
                    sample = fd1
                    ref = fd2
                idsymtg = sample[5:]
                indtg1 = self.findind(idsymtg,ind)
                idsymtg = ref[5:]
                indtg2 = self.findind(idsymtg,ind)
                oprtr.append('relerr')
                inpfd.append(indtg1)
                inpfd.append(indtg2)
                return (inpfd,oprtr)
            pat = re.search(' *100\*\((input[0-9a-zA-Z]+) *- *(input[0-9a-zA-Z]+)\)/ *(input[0-9a-zA-Z]+)',inputf)
            if pat != None:
                fd1 = pat.group(1)
                fd2 = pat.group(2)
                fd3 = pat.group(3)
                if fd1==fd3:
                    sample = fd2
                    ref = fd1
                else:
                    assert fd2==fd3, "Unsupported Format"
                    sample = fd1
                    ref = fd2
                idsymtg = sample[5:]
                indtg1 = self.findind(idsymtg,ind)
                idsymtg = ref[5:]
                indtg2 = self.findind(idsymtg,ind)
                oprtr.append('relerr')
                inpfd.append(indtg1)
                inpfd.append(indtg2)
                return (inpfd,oprtr)
            pat =re.search(' *VOLUME\((input[a-zA-Z0-9]+)\)',inputf)
            if pat != None:
                inpstr = pat.group(1)
                idsymtg = inpstr[5:] if inpstr[-1] != 'n' else inpstr[5:-1]
                indtg = self.findind(idsymtg,ind)
                oprtr.append('volume')
                inpfd.append(indtg)
                return (inpfd,oprtr)
            else:
                return self.tokenize(inputf.strip(),ind)
      
    def tokenize(self,inp,ind):
        oprtr=[]
        inpfd=[]
        while (len(inp)>0):
            if inp[0] == " ":
                inp=inp[1:]
            elif inp[0].isdigit():
                strnum = ''
                for t in inp:
                    if t.isdigit():
                        strnum += t 
                    else:
                        break
                inp=inp.lstrip(strnum)
                inpfd.append('c'+strnum)
            elif inp[0] in ['+','-','*','/','^',')','(']:
                oprtr.append(inp[0])
                inp=inp[1:]
            elif inp[:5]=='input':
                pat = re.search('^([0-9a-zA-Z]+)',inp[5:])
                assert pat != None, "Must have an identity symbol"
                idensym=pat.group(1)
                inp = inp[5:].lstrip(idensym)
                if idensym[-1]=='n':
                    idensym=idensym[:-1]
                idtg=self.findind(idensym,ind)
                inpfd.append(idtg)
        return (inpfd,oprtr)

    def findind(self,idsymtg,ind):
        indt = ind - 1
        indtg = ind
        while (indt >= 0):
            idensymt = self.part[indt]+self.questionNum[indt]+self.moduleNum[indt]
            if idsymtg == idensymt:
                indtg = indt
                break
            indt -= 1
#        assert indtg != ind, "Unrecognizable input field!" 
        return indtg

    def getquestp(self,ind):
        tol = self.answer[ind]
        pat = re.search('([0-9]+[0-9.]*\**o*u*t*p*u*t*[0-9a-zA-Z]*) *<= *(input[0-9a-zA-Z]+) *<= *([0-9]+[0-9.]*\**o*u*t*p*u*t*[0-9a-zA-Z]*)',tol)
        if pat == None:
            pat = re.search('output[0-9a-zA-Z]+ * [+-] *([0-9.]+) *<= *(input[0-9a-zA-Z]+) *<= *output[0-9a-zA-Z]+ * [+-] *([0-9.]+)',tol)
            assert pat != None,"Must match a pattern til now!"
        fd=[]
        fd.append(pat.group(1))
        fd.append(pat.group(2))
        fd.append(pat.group(3))
        inpstr = fd[1]
        idensymt = self.part[ind]+self.questionNum[ind]+self.moduleNum[ind]
        if inpstr == 'input'+idensymt:
            questp = 'one_num_input'
        elif inpstr == 'input'+idensymt+'n':
            questp = 'three_num_input'
        return questp

    def gettol(self,ind):
        tol = self.answer[ind]
        pat = re.search('([0-9]+[0-9.]*\**o*u*t*p*u*t*[0-9a-zA-Z]*) *<= *(input[0-9a-zA-Z]+) *<= *([0-9]+[0-9.]*\**o*u*t*p*u*t*[0-9a-zA-Z]*)',tol)
        if pat == None:
            pat = re.search('output[0-9a-zA-Z]+ * [+-] *([0-9.]+) *<= *(input[0-9a-zA-Z]+) *<= *output[0-9a-zA-Z]+ * [+-] *([0-9.]+)',tol)
            assert pat != None,"Must match a pattern til now!"
            toll = float(pat.group(1))
            tolu = float(pat.group(3))
            print toll,tolu
            return toll,tolu
        fd=[]
        fd.append(pat.group(1))
        fd.append(pat.group(2))
        fd.append(pat.group(3))
        if '*output' in fd[0]:
            lfd = fd[0].split('*')
            toll = eval(lfd[0])
            ufd = fd[2].split('*')
            tolu = eval(ufd[0])

            tmp = lfd[1].strip()
            idsymtg = tmp[6:] if tmp[-1]!='n' else tmp[6:-1]
            tmp = fd[1].strip()                
            idsym = tmp[5:] if tmp[-1]!='n' else tmp[5:-1]
            if idsymtg != idsym:
                indtg = self.findind(idsymtg,ind)
                print "compared fields are different!"
                return (toll,tolu)
            else:
                return (toll,tolu)
        else:
            toll = eval(fd[0])
            tolu = eval(fd[2])
            return (toll, tolu)

    def getvolume(self):
        inds = 52
        indf = 60
        volume={}
        for ind in range(inds,indf+1):
            volume[eval(self.eqtext[ind])] = eval(self.answer[ind])
        return volume
