from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from login.models import MenuItem

safety = MenuItem(perm_id=Permission.objects.get(codename='can_view').pk, dispname="Laboratory Safety",name='lab_safety', target='navi_main',alt='Click to view the lab safety')
safety.save()
proc = MenuItem(perm_id=Permission.objects.get(codename='can_view').pk, dispname="General Experimental Procedures",name='exp_procedures', target='navi_main',alt='Click to view the lab procedures')
proc.save()
prelab = MenuItem(perm_id=Permission.objects.get(codename='can_view').pk, dispname="Prelab Presentation",name='prelab_pres', target='navi_main',alt='Click to view the prelab presentation')
prelab.save()
prequiz = MenuItem(perm_id=Permission.objects.get(codename='can_view').pk, dispname="Prelab Quiz",name='prelab_quiz', target='navi_main',alt='Click to view the prelab quiz')
prequiz.save()
postlab = MenuItem(perm_id=Permission.objects.get(codename='can_view').pk, dispname="Postlab Quiz",name='postlab_quiz', target='navi_main',alt='Click to view the postlab quiz')
postlab.save()
quizsc = MenuItem(perm_id=Permission.objects.get(codename='can_take').pk, dispname="Quiz Scores",name='quiz_scores', target='navi_main',alt='Click to view the quiz scores')
quizsc.save()
labsc = MenuItem(perm_id=Permission.objects.get(codename='can_take').pk, dispname="Postlab Scores",name='postlab_scores', target='navi_main',alt='Click to view the postlab scores')
labsc.save()
reports = MenuItem(perm_id=Permission.objects.get(codename='can_grade').pk, dispname="Reports",name='reports', target='navi_main',alt='Click to view the reports')
reports.save()
edit = MenuItem(perm_id=Permission.objects.get(codename='can_edit').pk, dispname="Edit",name='edit', target='navi_main',alt='Click to edit quizzes')
edit.save()
