from django.contrib.postgres.fields import ArrayField, JSONField
import json
from django.db import models
from users.models import Profile


class Plan(models.Model):
    TYPE_CHOICES = (
        ("monthly", "Per Month"),
        ("yearly", "Per Year"),
    )

    stripe_product_id = models.CharField(max_length=225, blank=True, null=True)
    name = models.CharField(max_length=122)
    credit = models.PositiveIntegerField()
    plan_type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES
    )
    plan_cost = models.PositiveIntegerField()
    plan_features: list[str] = models.TextField(
        blank=True, null=True, help_text="""List should be comma separed. Example: ["Feat 1", "Feat 2", "Feat 3"]""")

    def __str__(self) -> str:
        return f"{self.name} - | {self.plan_type} - ${self.plan_cost}"

    @property
    def plan_feat_list(self):
        jsLoadsList = json.loads(self.plan_features)
        # all_feat = [f for f in jsLoadsList]
        return jsLoadsList


class Subscription(models.Model):
    customer_id = models.CharField(max_length=220, blank=True, null=True)
    sub_id = models.CharField(max_length=220, blank=True, null=True)
    user = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name='subs')
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    active = models.BooleanField(default=False)
    start = models.DateTimeField(auto_now_add=True)
    end = models.DateTimeField(blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.user.user.username} | {self.plan.name}"
