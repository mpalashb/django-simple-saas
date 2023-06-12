from django import forms
from general.models import Plan


class PlanForm(forms.ModelForm):
    plan_features = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}), help_text="""List should be comma separed. Example: ["Feat 1", "Feat 2", "Feat 3"]""")
    # plan_features = forms.Textarea(attrs={'class': 'form-control'})

    class Meta:
        model = Plan
        fields = "__all__"
