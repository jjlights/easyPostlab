#import django
from django.utils import timezone
from login.models import UserTable, SecurityPermission, SecurityGroup_User

p = SecurityPermission(permissionName='unrestricted',descriptionId=19060)
p.save()
p = SecurityPermission(permissionName='registered',descriptionId=19061)
p.save()
p = SecurityPermission(permissionName='SCHOOL',descriptionId=19062)
p.save()
p = SecurityPermission(permissionName='faculty',descriptionId=19063)
p.save()
p = SecurityPermission(permissionName='students&faculty',descriptionId=19064)
p.save()
p = SecurityPermission(permissionName='administrators',descriptionId=19065)
p.save()

#Dummy Data of UserTable SecurityGroup_User for Test
u = UserTable(fullName='Ruby Rails',dispName='ruby',email='ruby@rails.org',password='visit',added_date=timezone.now())
u.save()
u = UserTable(fullName='Hacker Chem',dispName='hacker',email='hacker@ucdavis.edu',password='secure',added_date=timezone.now())
u.save()
u = UserTable(fullName='Foo Bar',dispName='foobar',email='foobar@dummy.com',password='dummy',added_date=timezone.now())
u.save()
u = UserTable(fullName='Oreo Nabisco',dispName='oreo',email='oreo@nabisco.com',password='cookie',added_date=timezone.now())
u.save()
u = UserTable(fullName='Python Django',dispName='pydjango',email='py@django.org',password='web',added_date=timezone.now())
u.save()

su = SecurityGroup_User(user=UserTable.objects.get(dispName="ruby"),securityPermsId=SecurityPermission.objects.get(descriptionId=19060))
su.save()

su = SecurityGroup_User(user=UserTable.objects.get(dispName="foobar"),securityPermsId=SecurityPermission.objects.get(descriptionId=19061))
su.save()

su = SecurityGroup_User(user=UserTable.objects.get(dispName="hacker"),securityPermsId=SecurityPermission.objects.get(descriptionId=19062))
su.save()

su = SecurityGroup_User(user=UserTable.objects.get(dispName="oreo"),securityPermsId=SecurityPermission.objects.get(descriptionId=19064))
su.save()

su = SecurityGroup_User(user=UserTable.objects.get(dispName="pydjango"),securityPermsId=SecurityPermission.objects.get(descriptionId=19065))
su.save()

