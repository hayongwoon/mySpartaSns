from django.shortcuts import render, redirect
from .models import TweetModel, TweetComment
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, TemplateView

# Create your views here.
def home(request):
    user = request.user.is_authenticated
    if user:
        return redirect('/tweet')
    else:
        return redirect('/sign-in')

def tweet(request):
    if request.method == 'GET':#페이지를 보여주는 것은 GET
        user = request.user.is_authenticated
        if user:
            all_tweet = TweetModel.objects.all().order_by('-created_at') #-는 역순으로 정렬해서 준다는 의미
            return render(request, 'tweet/home.html', {'tweet':all_tweet})

        else:
            return redirect('/sign-in')

    elif request.method == 'POST':
        user = request.user # 지금 로그인 된 유저의 정보 다
        content = request.POST.get('my-content', '')
        tags = request.POST.get('tag','').split(',')

        if content == '':
            all_tweet = TweetModel.objects.all().order_by('-created_at')  # -는 역순으로 정렬해서 준다는 의미
            return render(request, 'tweet/home.html', {'error': '문자를 입력하세요!', 'tweet':all_tweet})
        else:
            my_tweet = TweetModel.objects.create(author=user, content=content)
            for tag in tags:
                tag = tag.strip()
                if tag != '':
                    my_tweet.tags.add(tag)

            my_tweet.save()
            return redirect('/tweet')

@login_required
def delete_tweet(request, id):
    my_tweet = TweetModel.objects.get(id=id)
    my_tweet.delete()
    return redirect('/tweet')

@login_required
def tweet_comment(request, id):
    tweet = TweetModel.objects.get(id=id)
    user = request.user
    comment = TweetComment.objects.filter(tweet_id=id)

    if request.method == 'GET':

        return render(request, 'tweet/tweet_detail.html', {'tweet':tweet, 'comment':comment})

    elif request.method == 'POST':
        tweet_comment = request.POST.get('comment', '')
        if tweet_comment == '':
            return render(request, 'tweet/tweet_detail.html', {'error': '문자를 입력하세요!', 'tweet':tweet, 'comment':comment})

        else:
            my_comment = TweetComment.objects.create(author=user, tweet=tweet, comment=tweet_comment)
            my_comment.save()
            return redirect('/tweet/comment/' + str(id))




@login_required
def delete_comment(request, id): #comment id 를 받은것이고
    my_comment = TweetComment.objects.get(id=id)
    tweet_id = my_comment.tweet_id #코멘트 id 에 해당하는 트윗에 아이디를 가져와서 redirect
    my_comment.delete()
    return redirect('/tweet/comment/'+str(tweet_id)) # tweet id 로 가야함.


class TagCloudTV(TemplateView):
    template_name = 'taggit/tag_cloud_view.html'


class TaggedObjectLV(ListView):
    template_name = 'taggit/tag_with_post.html'
    model = TweetModel

    def get_queryset(self):
        return TweetModel.objects.filter(tags__name=self.kwargs.get('tag'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tagname'] = self.kwargs['tag']
        return context




