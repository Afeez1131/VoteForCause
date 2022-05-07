from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib import messages
from django.urls import reverse_lazy
from allauth.account.views import PasswordChangeView, LoginView, SignupView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ProfileForm, CustomUserForm, CustomPasswordChange
from django.contrib.auth.decorators import login_required


class CustomLoginView(LoginView):
    """
    inheriting from the allauth LoginView,
    """

    template_name = "account/login.html"
    # success_url = reverse_lazy('profile')
    redirect_field_name = "next"


class CustomLogoutView(LogoutView):
    # template_name = 'account/logout.html'
    success_url = "account_login"

    def post(self, request):
        logout(request)
        return redirect("account_login")

    def get(self, request):
        return render(request, "account/logout.html")


class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    def get_success_url(self):
        success_url = reverse_lazy("home")
        messages.info(self.request, "Password changed succesfully")
        return success_url


@login_required
def ProfileView(request):
    user = request.user
    if request.method == "POST":
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        user_form = CustomUserForm(request.POST, instance=request.user)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.warning(request, 'You can now start creating Cause!')
        else:
            messages.warning(request, "Error filling the form")
        return redirect("profile")
    else:
        profile_form = ProfileForm(instance=request.user.profile)
        user_form = CustomUserForm(instance=request.user)
    return render(
        request,
        "profile.html",
        {
            "profile_form": profile_form,
            "user_form": user_form,
            "user": user,
        },
    )


# def custom_signup_view(request):
#     User = get_user_model()
#     if request.method == 'POST':
#         user_form = CustomRegistrationForm(request.POST)
#         profile_form = ProfileForm(request.POST)
#         if user_form.is_valid():
#             username = user_form.cleaned_data['username']
#             print('username ', username)
#             if profile_form.is_valid():
#                 phone_number = profile_form.cleaned_data['phone_number']
#                 print(phone_number)
#             # return redirect(reverse_lazy('account_login'))
#         else:
#             print('Errorrooo')
#             # return render(request, 'account/signup.html', {'user_form': user_form,
#             #                                                'profile_form': profile_form})
#     else:
#         user_form = CustomRegistrationForm()
#         profile_form = ProfileForm()
#
#     return render(request, 'account/signup.html', {'user_form': user_form,
#                                                    'profile_form': profile_form})


class CustomSignupView(SignupView):
    template_name = "account/signup.html"
    redirect_field_name = "next"

    def dispatch(self, request, *args, **kwargs):
        # will redirect to the home page if a user tries to access the register page while logged in
        if request.user.is_authenticated:
            return redirect("home")

        # else process dispatch as it otherwise normally would
        return super(CustomSignupView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        self.user = form.save(self.request)
        messages.info(self.request, "Registration Successfull, Login...")
        return redirect("account_login")
