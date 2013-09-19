#generate the prelab questions
from prelabq.models import QuizItems
from django import forms
import random

def choiceItem(question):
    return [(idx, q) for idx, q in enumerate(question.choices)]

class PrelabForm(forms.Form):
    def __init__(self, qchoose, *args, **kwargs):
        super(PrelabForm, self).__init__(*args, **kwargs)
        data = kwargs.pop('data',None)
        #query_set = QuizItems.objects.filter(id__in=[q.id for q in qchoose])
        if data is None:
        #q=qchoose[0]
        #self.fields['new'] = forms.ChoiceField(required=True,label=q.question,widget=forms.RadioSelect(),choices=choiceItem(q))
            for q in qchoose:
                self.fields[str(q.id)] = forms.ChoiceField(required=False,label=q.question,widget=forms.RadioSelect(),choices=choiceItem(q))
