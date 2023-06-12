from typing import Any, Optional
from django.db import models
from django.forms import TextInput
from django.forms import (
    ModelForm, CharField, Textarea,
)
from django.contrib import admin
from general.models import (
    Plan, Subscription
)
from general.forms import PlanForm


class FeatModel(admin.ModelAdmin):
    form = PlanForm
    change_form_template = "admin/feat_change_form.html"

    def get_form(self, request: Any, obj: Any | None = ..., change: bool = ..., **kwargs: Any) -> Any:
        print('---------------------------')
        print(f'Get form {request.POST.get("ttt")}')
        print('---------------------------')
        form_obj = super().get_form(request, obj, change, **kwargs)

        return form_obj


admin.site.register(Plan, FeatModel)
# admin.site.register(Plan)
admin.site.register(Subscription)
