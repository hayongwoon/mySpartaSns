from django.contrib import admin
from .models import UserModel
#.은 현재위치에 있는 것을 말함
# Register your models here.
admin.site.register(UserModel) # 이 코드가 나의 UserModel을 Admin에 추가 해 줍니다