from django.db import models
from django.contrib.auth.models import User


class CheckedProposal(models.Model):
    user = models.ForeignKey(
        'Profile', on_delete=models.CASCADE, related_name='checked_proposal')
    credit_cost = models.CharField(max_length=10, blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"User: {self.user.user} | Primary Key Of Checked Proposal: {self.pk}"


class GeneratedProposal(models.Model):
    user = models.ForeignKey(
        'Profile', on_delete=models.CASCADE, related_name='proposals')
    cover_leter = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"User: {self.user.user} | Primary Key Of Proposal: {self.pk}"


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.DO_NOTHING, related_name='profile'
    )
    email = models.EmailField(max_length=225, unique=True)

    first_name = models.CharField(max_length=125)  # added new
    last_name = models.CharField(max_length=125)  # added new
    # pic = models.ImageField(default='', blank=True, null=True)
    company = models.CharField(max_length=125)  # added new
    credit = models.PositiveIntegerField(default=50, blank=True, null=True)

    @property
    def active_sub(self):
        return self.subs.all().last()

    def __str__(self) -> str:

        if not self.subs.all().last():
            return f"Profile {self.pk} | User {self.user.username} | No Active subscription"

        return f"""Profile {self.pk} | User {self.user.username} 
        | Subscription - {self.subs.all().last().plan.name} - {self.subs.all().last().plan.plan_type} ${self.subs.all().last().plan.plan_cost} """


# class UserHistory(models.Model):
#     words = models.ForeignKey('GenWord', on_delete=models.CASCADE)


# class BillingHistory(models.Model):
#     sub_plan = None  # forenkey
#     ref_id = None
#     plan_type = None
#     purchase_date = None
#     cancel_date = None


# class GenWord(models.Model):
#     title = None
#     desc = None
#     score = None
