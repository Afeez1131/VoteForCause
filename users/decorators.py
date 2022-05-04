from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.contrib import messages


def profile_is_edited(function):
    '''
    Will check to see if the profile of a user has been edited, it is expected before a user can
    create a cause.
    if not, displays a message informing the user about the need to edit the profile and provide
    the other details before user can be permitted to create a cause.
    '''
    def wrap(request, *args, **kwargs):
        User = request.user
        if User.profile.phone_number == '' and User.profile.nationality == '':
            # request.next = 'cause_create'
            messages.warning(request, f'You need to update your profile before you can create a '
                                      'Cause.')
            return redirect('profile')
        else:
            return function(request, *args, **kwargs)
    return wrap