from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Profile, Post, Like, Comment
from django_messages.models import Message
from .forms import ProfileForm, CommentForm
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from .forms import PostForm
from django.http import HttpResponseRedirect, HttpResponse
from django.db.models import Q
from friendship.models import Friend, Follow
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.utils.translation import gettext
import re
import base64
import io
from PIL import Image

# Create your views here.
def home(request):
    return render(request, 'worldlink/home.html')

@login_required
def profile(request):
    name = None
    profile = None
    bposts = Post.objects.filter(author=request.user).order_by('-published_date')
    if request.user.is_authenticated():
        name = request.user.username
        if(Profile.objects.filter(user=request.user).order_by('-id')):
            profile = Profile.objects.filter(user=request.user).order_by('-id')[0]
        if(len(Profile.objects.filter(user=request.user).order_by('-id')) >= 2):
            toDel = Profile.objects.filter(user=request.user).order_by('-id')[2:]
            for td in toDel:
                td.delete()
    followers = Follow.objects.followers(request.user)
    following = Follow.objects.following(request.user)
    print(followers)
    print(following)
    return render(request, 'worldlink/profile.html', {'title': 'My Profile', 'name': name, 'profile': profile, 'bposts': bposts, 'followers': followers, 'following': following}) #, 'followers': followers, 'following': following

@login_required
def edit_profile(request):
    if request.method=='POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = str(request.user)
            '''if(Profile.objects.filter(user=request.user).order_by('-id') and (str(Profile.objects.filter(user=request.user).order_by('-id')[0].image.url) != 'static/images/profile-default.png')):
                print("Hi")
                if (str(Profile.objects.filter(user=request.user).order_by('-id')[0].image_url) != 'images/profile-default.png'):
                    print(str(Profile.objects.filter(user=request.user).order_by('-id')[0].image_url))
                    profile = Profile.objects.filter(user=request.user).order_by('-id')[0]
                    post.image_url = str(profile.image_url)
                    post.image = Profile.objects.filter(user=request.user).order_by('-id')[0].image
            else:
                #print(post.image.url)'''
            if(Profile.objects.filter(user=request.user).order_by('-id')):
                '''if(str(post.image.url) == 'static/images/profile-default.png'):
                    post.image_url = str(post.image.url)[7:]'''
                #else:
                if (post.image.url != str(Profile.objects.filter(user=request.user).order_by('-id')[0].image.url) and post.image.url != 'static/images/profile-default.png'):
                    post.image_url = ''.join(('images/', str(post.image.url)))
                else:
                    post.image = Profile.objects.filter(user=request.user).order_by('-id')[0].image
                    profile = Profile.objects.filter(user=request.user).order_by('-id')[0]
                    post.image_url = str(profile.image_url)
            else:
                post.image_url = str(post.image.url)[7:]
                #print(post.image_url)
            post.save()
            return redirect('profile')
    else:
        if(Profile.objects.filter(user=request.user).order_by('-id')):
            profile = Profile.objects.filter(user=request.user).order_by('-id')[0]
            url = profile.url
            name = profile.name
            date_of_birth = profile.date_of_birth
            education = profile.education
            hobbies = profile.hobbies
            image = profile.image
            #print(profile.image_url)
            #print(image_url)
            form = ProfileForm(initial={'url': url, 'name':name, 'date_of_birth': date_of_birth, 'hobbies': hobbies, 'education': education, 'image': image})
        else:
            form = ProfileForm()
    return render(request, 'worldlink/edit_profile.html', {'form': form})

def contact(request):
    return render(request, 'worldlink/contact.html')

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    return render(request, 'worldlink/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'worldlink/post_detail.html', {'post': post})

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            if post.image:
                post.image_url = ''.join(('images/', str(post.image.url)))
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'worldlink/post_edit.html', {'form': form})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            if post.image:
                post.image_url = ''.join(('images/', str(post.image.url)))
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'worldlink/post_edit.html', {'form': form})

def post_delete(request, pk):
    p = Post.objects.get(pk=pk)
    p.delete()
    return HttpResponseRedirect('/newsfeed')
'''
def upload_pic(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            m = Profile.objects.filter(user=request.user).order_by('-id')[0]
            m.model_pic = form.cleaned_data['image']
            m.save()
            return HttpResponse('image upload success')
    return HttpResponseForbidden('allowed only via POST')
'''
def search(request):
    if request.method == 'GET':
        search_query = request.GET.get('q', None)
        search_results = Profile.objects.filter(Q(user__icontains=search_query) | Q(name__icontains=search_query))
        final_list = []
        if len(search_results) >= 2:
            for i in range(len(search_results)-1):
                print(search_results[i].user, search_results[i+1].user)
                if search_results[i].user == search_results[i+1].user:
                    continue
                else:
                    final_list.append(search_results[i])
        else:
            final_list = search_results
        if len(search_results) >= 2 and search_results[len(search_results)-2].user == search_results[len(search_results)-1].user:
            final_list.append(search_results[len(search_results)-2])
        #print(search_results)
        for i in search_results:
            print(i.user)
        print()
        for i in final_list:
            print(i.user)
        return render(request, 'worldlink/search_result.html', {'search_results': final_list})

def viewprofile(request, user, val=None):
    name = None
    profile = None
    print("hi")
    user = str(user)
    print(user)
    bposts = Post.objects.filter(author__username=user).order_by('-published_date')
    if request.user.is_authenticated():
        name = user
        if(Profile.objects.filter(user=user).order_by('-id')):
            profile = Profile.objects.filter(user=user).order_by('-id')[0]
        if(len(Profile.objects.filter(user=user).order_by('-id')) >= 2):
            toDel = Profile.objects.filter(user=user).order_by('-id')[2:]
            for td in toDel:
                td.delete()
    profile_to_follow = User.objects.filter(username=user).order_by('-id')[0]
    if request.user in Follow.objects.followers(profile_to_follow):
        val = '1'
    return render(request, 'worldlink/profile.html', {'title': name, 'name': name, 'profile': profile, 'bposts': bposts, 'val': val})

def follow_user(request, user_profile):
    profile_to_follow = User.objects.filter(username=user_profile).order_by('-id')[0]
    if request.user not in Follow.objects.followers(profile_to_follow):
        Follow.objects.add_follower(request.user, profile_to_follow)
        print("hiugkug")
        return viewprofile(request, user_profile, 1)
    else:
        return viewprofile(request, user_profile)

def unfollow_user(request, user_profile):
    profile_to_follow = User.objects.filter(username=user_profile).order_by('-id')[0]
    if request.user in Follow.objects.followers(profile_to_follow):
        Follow.objects.remove_follower(request.user, profile_to_follow)
    return viewprofile(request, user_profile)

def like(request, pk):
    posts=get_object_or_404(Post,pk=pk)
    new_like, created = Like.objects.get_or_create(user=request.user,post=posts)
    #posts.likes= p.like_set.all().count()
    if not created:
        new_like.delete()
    return HttpResponseRedirect('/newsfeed')

def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'worldlink/add_comment.html', {'form': form})

@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('post_detail', pk=comment.post.pk)

def meme_gen(request):
    return render(request, 'worldlink/meme_gen.html')

def save_image(request):
    if request.method == "POST" and request.is_ajax():
        dataURL =  request.POST['dataURL'].partition('base64,')[2]
        '''
        imgstr = re.search(r'base64,(.*)', dataURL).group(1)
        output = open('output.png', 'w')
        output.write(imgstr)
        output.close()
        return redirect('meme_gen')
        '''
        pic = io.BytesIO()
        image_string = io.BytesIO(base64.b64decode(dataURL))
        image = Image.open(image_string)
        image.save(pic, image.format, quality = 100)
        pic.seek(0)
        return JsonResponse({ 'success': True })

def Notifications(request):
    if request.method == 'GET':
        notifications=None
        like_notifications=None
        notifications=Message.objects.filter(recipient=request.user).order_by('-sent_at')
        like_notifications=Like.objects.filter(post__author__exact=request.user)
        comment_notifications=Comment.objects.filter(post__author__exact=request.user)
        count=len(notifications)+len(like_notifications)+len(comment_notifications)
        return render(request, 'worldlink/notifications.html', {'notifications':notifications,'like_notifications':like_notifications,'comment_notifications':comment_notifications,'count':count})


def update_like(request):
    if request.method == "POST" and request.is_ajax():
        pk =  request.POST['pk']
        posts=get_object_or_404(Post,pk=pk)
        new_like, created = Like.objects.get_or_create(user=request.user,post=posts)
        #posts.likes= p.like_set.all().count()
        if not created:
            new_like.delete()
        #b = Like.objects.get(user=request.user,post=posts)
        num = posts.like_set.all().count()
        #print(type(num))
        return JsonResponse({ 'num': num , 'pk': posts.pk})

from django.views.generic import ListView

class ListProfileView(ListView):

    model = Profile
    template_name = 'profile_list.html'
