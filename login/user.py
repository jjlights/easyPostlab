from django.contrib.auth.models import User
usr = User.objects.create_user('ruby','ruby@rails.org','pwd')
usr = User.objects.create_user('foo','foo@bar.org','pwd')
usr = User.objects.create_user('java','java@j2ee.org','pwd')
usr = User.objects.create_user('js','js@nodejs.org','pwd')
usr = User.objects.create_user('lang','lang@framework.org','pwd')
usr = User.objects.create_user('python','python@django.org','pwd')
usr.is_staff = True
usr.save()
