from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType

test = Group(name='Unrestricted')
test.save()
guest = Group(name='Guest')
guest.save()
student = Group(name='Student')
student.save()
ta = Group(name='TA')
ta.save()
headta = Group(name='HeadTA')
headta.save()
faculty = Group(name='Faculty')
faculty.save()
admin = Group(name='Administrator')
admin.save()

ctmodel = ContentType.objects.get(app_label='auth',model='User')
can_view = Permission(name='Can View',codename='can_view',content_type=ctmodel)
can_view.save()
can_take = Permission(name='Can Take Quiz',codename='can_take',content_type=ctmodel)
can_take.save()
can_grade = Permission(name='Can Grade Quiz',codename='can_grade',content_type=ctmodel)
can_grade.save()
can_edit = Permission(name='Can Edit',codename='can_edit',content_type=ctmodel)
can_edit.save()
can_admin = Permission(name='Can Admin',codename='can_admin',content_type=ctmodel)
can_admin.save()

guest.permissions.add(can_view)
student.permissions = [can_view, can_take]
ta.permissions = [can_view, can_take, can_grade]
headta.permissions = [can_view, can_take, can_grade]
faculty.permissions = [can_view, can_take, can_grade, can_edit]
admin.permissions = [can_view, can_take, can_edit, can_admin]

ruby = User.objects.get(username='ruby')
foo = User.objects.get(username='foo')
java = User.objects.get(username='java')
js = User.objects.get(username='js')
lang = User.objects.get(username='lang')
python = User.objects.get(username='python')

ruby.groups.add(guest)
foo.groups.add(student)
java.groups.add(ta)
js.groups.add(headta)
lang.groups.add(faculty)
python.groups.add(admin)
