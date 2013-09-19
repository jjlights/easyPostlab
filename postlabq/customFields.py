from django.db import models
import types, operator, math

class EquationField(models.Field):
    def __init__(self, inpField, caltype, *args, **kwargs):
        inp = [inp.answer for inp in inpField]
        oprtr = get_operator(caltype)
        super(EquationField,self).__init__(*args, **kwargs)
