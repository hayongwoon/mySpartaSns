from django.shortcuts import render, redirect
from django.contrib import messages
from .models import UserModel
from django.http import HttpResponse
from django.contrib.auth import get_user_model #사용자가 데이터베이스에 있는지 검사하는 함수
from django.contrib import auth
from django.contrib.auth.decorators import login_required

# Create your views here.
def sign_up_view(request):
    if request.method == 'GET':
        user = request.user.is_authenticated
        if user:
            return redirect('/')
        else:
            return render(request, 'user/signup.html')

    elif request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        password2 = request.POST.get('password2', '')
        bio = request.POST.get('bio', '')

        if password != password2:
            #패스워드가 같지 않다고 알람
            return render(request, 'user/signup.html', {'error':'패스워드를 확인하세요!'})

        else:
            if username == '' or password == '':
                return render(request, 'user/signup.html', {'error':'사용자 이름과 비밀번호는 필수 값 입니다.'})


            exist_user = get_user_model().objects.filter(username=username)
            if exist_user:
                return render(request, 'user/signup.html', {'error':'사용자가 존재합니다.'})
            else:
                UserModel.objects.create_user(username=username, password=password, bio=bio)
                #유저 생성 더 간단하게 하는 메소드, 굳이 클래스 사용 안해도 됨.

                return redirect('/sign-in')


def sign_in_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        me = auth.authenticate(request, username=username, password=password)
        # 사용자의 패스워드가 장고가 알아서 암호화를 한다. 떄문에 그냥 비밀번호를 가져와 비교하면
        # 에러가 나므로 authenticate 메소드를 활용
        # 이 메소드는 알아서 해독을 해주고 그게 입력한 비밀번호와 비교까지 해주고 또 그게 사용자가 맞는지까지 한번에 확인
        if me is not None: #비어있지 않다면
            auth.login(request, me)
            #request.session['user'] = me.username #session user 라는 공간에 me.username을 저장하겠다는 의미
            return redirect('/')
        else:
            return render(request, 'user/signin.html', {'error':'유저 혹은 패스워드를 확인하세요'})

    elif request.method == 'GET':
        user = request.user.is_authenticated
        if user:
            return redirect('/')
        else:
            return render(request, 'user/signin.html')

@login_required  #로그인이 되어있어야만 작용되는 함수라는 의미
def logout(request):
    auth.logout(request)
    return redirect('/')

# user/views.py

@login_required
def user_view(request):
    if request.method == 'GET':
        # 사용자를 불러오기, exclude와 request.user.username 를 사용해서 '로그인 한 사용자'를 제외하기
        user_list = UserModel.objects.all().exclude(username=request.user.username) #나를 제외한 나머지 유저들의 정보를 가져온다.
        return render(request, 'user/user_list.html', {'user_list': user_list})


@login_required
def user_follow(request, id):
    me = request.user
    click_user = UserModel.objects.get(id=id)
    if me in click_user.followee.all():
        click_user.followee.remove(request.user)
    else:
        click_user.followee.add(request.user)
    return redirect('/user')