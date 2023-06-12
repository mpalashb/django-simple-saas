from django.contrib import admin
from users.models import (
    Profile, GeneratedProposal, CheckedProposal
)


class ProfileModel(admin.ModelAdmin):
    list_display = (
        'id',
        'email',
        'user',
        'credit',
        'check_active_subs',
    )

    @admin.display(empty_value="???")
    def check_active_subs(self, obj):
        if not obj.subs.all().last():
            return f"Profile {obj.pk} - {obj.email}| No Active subscription"

        return f"""Subscription - {obj.subs.all().last().plan.name} - {obj.subs.all().last().plan.plan_type} ${obj.subs.all().last().plan.plan_cost} """


admin.site.register(CheckedProposal)
admin.site.register(GeneratedProposal)
admin.site.register(Profile, ProfileModel)
