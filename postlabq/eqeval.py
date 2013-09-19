# evaluation of calculations

import types, operator, math

def extendop(op,a,b):
    print "type a:",type(a)
    print "type b:",type(b)

    if type(a) is types.FloatType and type(b) is types.FloatType:
        return op(a,b)
    else:
        if type(a) is types.FloatType:
            lb=b
            la = [a]*len(b)
        elif type(b) is types.FloatType:
            la=a
            lb = [b]*len(a)
        elif len(a) != len(b):
            print "Two list length not matched"
        else:
            #raise MyError("UncatchedType")
            return [op(ia,ib) for (ia,ib) in zip(a,b)]
        return [op(ia,ib) for (ia,ib) in zip(la,lb)]

def eadd(a,b):
    return extendop(oprtor.add,a,b)

def esub(a,b):
    return extendop(operator.sub,a,b)

def emul(a,b):
    return extendop(operator.mul,a,b)

def ediv(a,b):
    print "a:",a
    print "b:",b
    return extendop(operator.div,a,b)

def inv(num):
    if type(num) is types.FloatType:
        return 1.0/num
    else:
        return [1.0/ele for ele in num]

def log(num):
    if type(num) is types.FloatType:
        return math.log(num)
    else:
        return [math.log(ele) for ele in num]

def ave(lst):
    assert type(lst) is types.ListType, "need to have a list"
    return sum(lst)/len(lst)

def stddev(lst):
    assert type(lst) is types.ListType, "need to have a list"
    av = ave(lst)
    nlst = [math.pow(item-av,2) for item in lst]
    return sum(nlst)/(len(nlst)-1)

def relerr(a,b):
    assert type(a) is types.FloatType and type(b) is types.FloatType, "Two variables should be float"
    return 100*math.fabs(a-b)/b

def pctg(a,b):
    assert type(a) is types.FloatType and type(b) is types.FloatType, "Two variables should be float"
    return 100*(a-b)/b

def conflim(a,n):
    assert type(a) is types.FloatType and type(n) is types.FloatType, "Variables types are not correct"
    return conf[int(n)]*a/n

def volume(temp):
    assert type(temp) is types.FloatType, "Variables types are not correct"
    return vol[temp]

vol = {  # volume of water at different temperature
        18.0: 1.0024, 
        19.0: 1.0026, 
        20.0: 1.0028, 
        21.0: 1.003, 
        22.0: 1.0033, 
        23.0: 1.0035, 
        24.0: 1.0037, 
        25.0: 1.004, 
        26.0: 1.0043,
        }

conf = {    # 90% confident limit for different number of sample
        1:1.0,
        2:2.3,
        3:2.920,
        }

oprtor = ['+','-','*','/','log','inv','ave','stddev','(',')']
ops = {
        #"+": operator.add,
        #"-": operator.sub,
        #"*": operator.mul,
        #"/": operator.div,
        "+": eadd,
        "-": esub,
        "*": emul,
        "/": ediv,
        "inv":inv,
        "log": log,
        "ave": ave,
        "stddev": stddev,
        "relerr": relerr,
        "pctg": pctg,
        "conflim": conflim,
        "volume": volume,
        }

binaryops = ["+","-","*","/"]

ops_rank = {
        "+":1,
        "-":1,
        "*":2,
        "/":2,
        }

def precedence(a,b):
    opa = ops_rank[a]
    opb = ops_rank[b]
    if opa >= opb:
        return True
    else:
        return False

def binaryeval(inp,oprtr,a):
    if oprtr == []:
        assert len(inp) >= 2, "expression not complete:two operands are needed to evaluate!"
        res = ops[a](inp.pop(0),inp.pop(0))
        inp.insert(0,res)
        return
    if oprtr[0] == ")":
        assert len(inp) >= 2, "expression not complete:two operands are needed to evaluate!"
        res = ops[a](inp.pop(0),inp.pop(0))
        inp.insert(0,res)
    elif oprtr[0] == "(":
        tmp = inp[1:]
        evaluate(tmp, oprtr)
        del inp[1:]
        inp.extend(tmp)
        binaryeval(inp,oprtr,a)
    else:
        b = oprtr.pop(0)
        if b not in binaryops:
            op = ops[b]
            assert len(inp[1:]) >= 1, "expression not complete:one operand is needed to evaluate!"
            res = op(inp.pop(1))
            inp.insert(1,res)
            binaryeval(inp,oprtr,a)
        else:
            if len(oprtr)>=1 and oprtr[0] == "(":
                tmp = inp[2:]
                evaluate(tmp,oprtr)
                del inp[2:]
                inp.extend(tmp)
                oprtr.insert(0,b)
                binaryeval(inp,oprtr,a)
                return
            if precedence(a,b):
                assert len(inp) >= 2, "expression not complete:two operands are needed to evaluate!"
                res = ops[a](inp.pop(0),inp.pop(0))
                inp.insert(0,res)
                oprtr.insert(0,b)
            else:
                assert len(inp) >= 3, "expression not complete:three operands are needed to evaluate!"
                res = ops[b](inp.pop(1),inp.pop(1))
                inp.insert(1,res)
                oprtr.insert(0,a)
    return

def evaluate(inp, oprtr):
    while (len(oprtr)>=1):
        a = oprtr.pop(0)
        if a == "(":
            evaluate(inp,oprtr)
            return
        elif a == ")":
            return
        elif a not in binaryops:
            assert len(inp) >= 1, "expression not complete:at least one operand is needed to evaluate!"
            if a == "relerr":
                res = ops[a](inp.pop(0),inp.pop(0))
            elif a == "conflim":
                res = ops[a](inp.pop(0),inp.pop(0))
            else:
                res = ops[a](inp.pop(0))
            inp.insert(0,res)
        else:
            binaryeval(inp,oprtr,a)
    assert len(inp) == 1, "Evaluation Wrong"
    return inp[0]

def assertmsg(string):
    if type(string) == types.StringType:
        return "Unrecognized token: %s, only %s supported" %(tk,string)
    elif type(string) == types.ListType:
        pstr = ''
        for s in string:
            pstr += s+' '
        return "Unrecognized token: %s, only %s supported" %(tk,pstr)

def tokenize(inp):
    oprtr=[]
    oprd=[]
    while (len(inp)>0):
        c=inp[0]
        inp=inp[1:]
        if c in ['+','-','*','/','^',')','(']:
            oprtr.append(c)
        elif c=='a':
            t=inp[:2]
            inp = inp[2:]
            assert t=='ve', assertmsg(c+t,'ave')
            oprtr.append('ave')
        elif c=='i':
            t=inp[:2]
            inp = inp[2:]
            assert t=='nv', assertmsg(c+t,'inv')
            oprtr.append('inv')
        elif c=='l':
            t=inp[:2]
            inp = inp[2:]
            assert t=='og', assertmsg(c+t,'log')
            oprtr.append('log')
        elif c=='s':
            t=inp[:3]
            inp = inp[3:]
            if t=='qrt':
                oprtr.append('sqrt')
            else:
                assertmsg(c+t,'sqrt')
        elif c=='r':
            t=inp[:2]
            if t=='es':
                inp = inp[2:]
                assert inp[0]=='(',"Wrong Format"
                inp=inp[1:]
                ind = inp.find(')')
                assert ind != -1, "Wrong Format"
                oprd.append(inp[:ind])
                inp=inp[ind+1:]
            else:
                t=inp[:5]
                assert t=='elerr', assertmsg(c+t,'res,relerr')
                oprtr.append('relerr')
                inp = inp[5:]
        elif c=='s':
            t=inp[:5]
            assert t=='tddev', assertmsg('stddev')
            oprtr.append('stddev')
            inp=inp[5:]
        elif c.isdigit():
            ind=0
            while (ind < len(inp) and inp[ind].isdigit()):
                ind += 1
            num=inp[:ind]
            oprd.append(c+num)
            inp=inp[ind:]
        else:
            print "Unrecognized token: %s" %(c)
    return (oprd, oprtr)
