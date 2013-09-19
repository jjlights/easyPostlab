# display the postlabq pages
from postlabq.models import BaseQuestion, TextInputQuestion, ChoiceQuestion, CalQuestion
from django import forms

def choiceItem(question):
    return [(idx, q) for idx, q in enumerate(question.choices)]

class PostlabDisplay():
    def __init__(self, q, *args, **kwargs):
        if hasattr(q, 'textinputquestion') or hasattr(q,'calquestion'):
            self.fields[str(q.id)] = forms.FloatField(required=True,label=q.question,widget=forms.TextInput())
        elif hasattr(q,'choicequestion'):
            self.fields[str(q.id)] = forms.FloatField(required=True,label=q.question,widget=forms.TextInput())

class PostlabForm(forms.Form):
    def __init__(self, *args, **kwargs):
        q = kwargs.pop('question',None)
        super(PostlabForm, self).__init__(*args, **kwargs)
        if q is not None:
            qtype = q.ques
            if qtype.quesType == 'one_num_input':
                self.fields[str(qtype.id)+'-'+str(q.id)] = forms.FloatField(required=True,
                        label=q.inputLabel[0],
                        widget=forms.TextInput())
            elif qtype.quesType == 'three_num_input':
                for i in range(3):
                    self.fields[str(qtype.id)+'-'+str(q.id)+'-'+str(i)] = forms.FloatField(required=True,
                        label=q.inputLabel[0],
                            widget=forms.TextInput())
            elif qtype.quesType == 'single_choice':
                self.fields[str(qtype.id)+'-'+str(q.id)] = forms.ChoiceField(required=True,
                        widget=forms.RadioSelect(),choices=choiceItem(q))
            elif qtype.quesType == 'multiple_choice':
                self.fields[str(qtype.id)+'-'+str(q.id)] = forms.MultipleChoiceField(required=True, widget=forms.CheckboxSelectMultiple(),choices=choiceItem(q))
            elif qtype.quesType == 'puretext':
                self.fields[str(qtype.id)+'-'+str(q.id)] = forms.CharField(required=False,label="",widget=forms.HiddenInput())
            elif qtype.quesType == 'freeresponse':
                self.fields[str(qtype.id)+'-'+str(q.id)] = forms.CharField(required=True,label="",widget=forms.Textarea)
            else:
                pass
