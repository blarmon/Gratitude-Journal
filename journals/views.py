from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login

from journals.forms import JournalForm
from journals.models import Journal


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
                return redirect('index')

        latest_three_journals = Journal.objects.all().order_by('-date')[:3]

        form = JournalForm
        context = {'title': 'Home', 'form': form, 'user_id': request.user.id, 'latest_three_journals': latest_three_journals}
        return render(request, 'journals/index.html', context)
    else:
        return redirect('explore')


def explore(request):
    public_journals = Journal.objects.filter(public=True)
    context = {'title': 'Explore', 'public_journals': public_journals}
    return render(request, 'journals/explore.html', context)


def profile(request, user_id):
    user_journals = Journal.objects.filter(user=request.user).order_by('-date')

    context = {'user_journals': user_journals}
    return render(request, 'journals/profile.html', context)

def journal_detail(request, journal_id):
    journal = Journal.objects.get(id=journal_id)

    context = {'journal': journal}
    return render(request, 'journals/journal_detail.html', context)


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    context = {'form': form}
    return render(request, 'registration/register.html', context)

