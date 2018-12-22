from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.db.models import Q

from journals.forms import JournalForm, RegistrationForm, RegistrationFormUserExtension
from journals.models import Journal, UserExtension


# Create your views here.
def index(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            redirect('index')
            form = JournalForm(request.POST)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.user = request.user
                instance.save()
                form.save_m2m()
                return redirect('index')
        latest_three_journals = Journal.objects.filter(user=request.user).order_by('-date')[:5]
        form = JournalForm
        context = {'title': 'Home', 'form': form, 'user_id': request.user.id, 'latest_three_journals': latest_three_journals}
        return render(request, 'journals/index.html', context)
    else:
        return redirect('explore')


def explore(request):
    context = {}
    if 'search_term' in request.GET:
        search_term = (request.GET['search_term'])
        journal_search_results = Journal.objects.filter(Q(title__icontains=search_term) | Q(body__icontains=search_term) | Q(tags__name__icontains=search_term)).filter(public=True).distinct()
        user_search_results = User.objects.filter(username__icontains=search_term).distinct()
        context.update({'search_term': request.GET['search_term'], 'journal_search_results': journal_search_results, 'user_search_results': user_search_results})
    public_journals = Journal.objects.filter(public=True).order_by('-date')[:10]
    context.update({'title': 'Explore', 'public_journals': public_journals})
    return render(request, 'journals/explore.html', context)


def profile(request, user_slug):
    context = {}
    user_profile = User.objects.get(userextension=UserExtension.objects.get(slug=user_slug))
    if user_profile == request.user:
        loggedin_user_profile = True
        user_journals = Journal.objects.filter(user=user_profile).order_by('-date')
        registration_form_user_extension = RegistrationFormUserExtension()
        context.update({'registration_form_user_extension': registration_form_user_extension})
    else:
        loggedin_user_profile = False
        user_journals = Journal.objects.filter(user=user_profile, public=True).order_by('-date')
    followed_by = False
    if request.user.is_authenticated:
        if request.user.userextension.follows.filter(user_id=user_profile.id):
            followed_by = True
    follows_users = []
    followed_by_users = []
    if loggedin_user_profile:
        follows_users = request.user.userextension.follows.all()
        followed_by_users = request.user.userextension.followed_by.all()
    context.update({'user_journals': user_journals, 'user_profile': user_profile, 'loggedin_user_profile': loggedin_user_profile, 'followed_by': followed_by, 'follows_users': follows_users, 'followed_by_users': followed_by_users})
    return render(request, 'journals/profile.html', context)


def edit_profile_image(request):
    if request.method == 'POST':
        registration_form_user_extension = RegistrationFormUserExtension(request.POST, request.FILES)
        if registration_form_user_extension.is_valid():
            request.user.userextension.user_image = registration_form_user_extension.cleaned_data['user_image']
            request.user.userextension.save()
            return redirect('/profile/' + request.user.userextension.slug)


def journal_detail(request, journal_slug):
    journal = Journal.objects.get(slug=journal_slug)
    logged_in_users_journal = False
    if request.user == journal.user:
        logged_in_users_journal = True
    context = {'journal': journal, 'logged_in_users_journal': logged_in_users_journal}
    return render(request, 'journals/journal_detail.html', context)


def follow_user(request):
    user_to_follow_or_unfollow = User.objects.get(username=request.POST['user_to_follow_or_unfollow'])
    if request.POST['data'] == 'Follow':
        request.user.userextension.follows.add(user_to_follow_or_unfollow.userextension)
    else:
        request.user.userextension.follows.remove(user_to_follow_or_unfollow.userextension)
    return HttpResponse("OK")


def feed(request):
    followed_users_extensions = request.user.userextension.follows.all()
    followed_users = User.objects.filter(userextension__in=followed_users_extensions)
    journals_from_followed = Journal.objects.filter(user__in=followed_users, public=True).order_by('-date')
    context = {'journals_from_followed': journals_from_followed}
    return render(request, 'journals/feed.html', context)


def delete_journal(request):
    Journal.objects.get(id=request.POST['journal_id']).delete()
    return redirect('index')


def register(request):
    if request.method == 'POST':
        registration_form = RegistrationForm(request.POST)
        registration_form_user_extension = RegistrationFormUserExtension(request.POST, request.FILES)
        if registration_form.is_valid() and registration_form_user_extension.is_valid():
            registration_form.save()
            username = registration_form.cleaned_data['username']
            password = registration_form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            user.userextension.user_image = registration_form_user_extension.cleaned_data['user_image']
            user.userextension.save()
            return redirect('index')
    else:
        registration_form = RegistrationForm()
        registration_form_user_extension = RegistrationFormUserExtension()
    context = {'registration_form': registration_form, 'registration_form_user_extension': registration_form_user_extension}
    return render(request, 'registration/register.html', context)