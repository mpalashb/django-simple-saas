from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import get_object_or_404
from general.models import Profile


class IsOwnerProfile(UserPassesTestMixin):
    def test_func(self) -> bool | None:
        # is_profile =  get_object_or_404(Profile, user=self.request.user)
        # is_profile = Profile.objects.get(user=self.request.user)
        is_profile = Profile.objects.filter(user=self.request.user).first()
        if not is_profile:
            return False
        return is_profile.user == self.request.user
