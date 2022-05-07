from django.shortcuts import render, get_object_or_404, redirect
from .models import Causes, VoteForCause
from .forms import CauseCreateForm, CauseUpdateForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .decorators import user_is_author, profile_is_edited
from django.contrib import messages
from taggit.models import Tag
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def home(request):
    '''
    The home view, it has the list of all causes
    '''
    causes = Causes.published.all()

    paginator = Paginator(causes, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)


    return render(request, "causes_list.html", {"causes": causes,
                                                'page_obj': page_obj,})


def search_for_cause(request):
    '''
    The view for searching for cause
    '''
    query = request.GET.get("query")
    if query:
        causes = Causes.published.filter(
            Q(title__icontains=query) | Q(body__icontains=query)
        )
        return render(request, "search_page.html", {'causes': causes,
                                                    'query': query})
    return render(request, "search_page.html", {})


def user_cause(request, username):
    '''
    the view to get all cause for a user passed as a url argument
    '''
    # user = username
    causes = Causes.published.filter(author__username=username)

    return render(request, 'user_cause.html', {'causes': causes,
                                               'user': username, })


def tag_view(request, tag_slug):
    """
    This will assist in filtering and listing causes by tags passed as argument using the tag_slug
    """
    causes = Causes.published.all()
    tag = get_object_or_404(Tag, slug=tag_slug)
    causes = causes.filter(tags__in=[tag])
    return render(request, "causes_list.html", {"causes": causes})


@login_required
@profile_is_edited
def create_cause(request):
    '''
    In order to create a cause, the user should be authenticated, and should have edited his or
    her profile.
    if Not, will be redirected to the profile page for editing
    '''
    if request.method == "POST":
        form = CauseCreateForm(request.POST)
        if form.is_valid():
            form.instance.author = request.user
            cause = form.save()
            print('Slug ', cause)

            return redirect(cause.get_absolute_url())
        else:
            return render(request, "cause_create.html", {"form": form})
    else:
        form = CauseCreateForm()
    return render(request, "cause_create.html", {"form": form})


def cause_detail(request, slug):
    """
    the detail view of each cause
    """
    cause = get_object_or_404(Causes, slug=slug, active=True)
    user = request.user
    if not request.user.is_authenticated:
        has_sign = None
    else:
        has_sign = VoteForCause.objects.filter(cause=cause, user=user).exists()

    causes = Causes.published.all().order_by("-created")[:4]
    '''
    i wrote a custom model manager published, which return the list of only published causes, 
    deleted (unpublished ) causes will be excluded.
    '''

    return render(
        request,
        "cause_detail.html",
        {
            "cause": cause,
            "causes": causes,
            'has_sign': has_sign
        },
    )


@login_required
@user_is_author
def cause_update(request, slug):
    '''
    User should be authenticated, and only the author of a cause can edit the cause
    '''
    cause = get_object_or_404(Causes, slug=slug, active=True)
    if request.method == "POST":
        form = CauseUpdateForm(request.POST, instance=cause)
        if form.is_valid():
            form.save()
            return redirect(cause.get_absolute_url())
    else:
        form = CauseUpdateForm(instance=cause)

    return render(
        request,
        "cause_update.html",
        {
            "form": form,
        },
    )


@login_required
@user_is_author
def cause_delete(request, slug):
    '''
    To delete a cause, user should be authenticated and only the author of a cause can delete a
    cause.
    Also, the cause is not deleted, but unpublished.
    '''
    cause = get_object_or_404(Causes, slug=slug, active=True)
    cause.active = False
    cause.save()
    return redirect("home")


@login_required
def cause_signed_userlist(request, slug):
    '''
    The view that return the list of all users that signed for a cause.
    '''
    cause = get_object_or_404(Causes, slug=slug, active=True)
    vfcs = VoteForCause.objects.filter(cause=cause)

    return render(request, 'cause_signed_list.html', {'cause': cause,
                                                      'vfcs': vfcs, })


@login_required
def add_sign_cause(request, slug):
    '''
    Adding signature to a cause, user should be authenticated, and cannot sign more than one.
    '''
    user = request.user
    cause = get_object_or_404(Causes, slug=slug, active=True)

    vote_for_cause = VoteForCause.objects.filter(Q(cause=cause) & Q(user=user))
    if vote_for_cause.exists():
        messages.warning(request, 'You added your signature for this cause already!')
    else:
        vote_for_cause, created = VoteForCause.objects.get_or_create(cause=cause, user=user,
                                                                     has_signed=True)
        if created:
            vote_for_cause.save()

    return redirect(cause.get_absolute_url())
