from dateutil.relativedelta import relativedelta
from django.db.models.signals import post_save
from django.dispatch import receiver
from general.models import (
    Subscription, Profile
)


# @receiver(post_save, sender=Profile)
# def save_credit_to_profile(sender, instance, created, **kwargs):

#     if created:
#         instance.credit = instance.subscription.plan.credit
#         instance.save()


@receiver(post_save, sender=Subscription)
def save_credit_to_profile(sender, instance, created, **kwargs):

    if created and instance.active:
        profile_instance = Profile.objects.get(id=instance.user.id)
        if instance.plan.plan_type == 'monthly':
            instance_date = instance.start
            adding_date_time = instance_date + relativedelta(months=1)
            instance.end = adding_date_time
            instance.save()

        if instance.plan.plan_type == 'yearly':
            instance_date = instance.start
            adding_date_time = instance_date + relativedelta(months=12)
            instance.end = adding_date_time
            instance.save()
        # print(profile_instance)
        if profile_instance:
            profile_instance.credit = int(
                profile_instance.credit) + int(instance.plan.credit)
            profile_instance.save()
