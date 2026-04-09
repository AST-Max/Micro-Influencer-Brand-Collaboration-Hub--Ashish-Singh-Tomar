from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Profile, Campaign



class InfluencerSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_influencer = True  # Tagging the user type
        if commit:
            user.save()
            Profile.objects.get_or_create(user=user)
        return user



class BrandSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_brand = True  # The key differentiator
        if commit:
            user.save()
        return user
    



class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'location', 'profile_picture', 'niche', 'instagram_handle', 'follower_count']
        
        # Adding widgets makes the form look professional like your screenshots
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Describe your content style...'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Lucknow'}),
            'niche': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Tech, Fashion, Food'}),
            'instagram_handle': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '@username'}),
            'follower_count': forms.NumberInput(attrs={'class': 'form-control'}),
        }



class CampaignForm(forms.ModelForm):
    class Meta:
        model = Campaign
        fields = ['title', 'description', 'budget', 'required_niche']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Summer Collection Launch'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'What do you need the influencer to do?'}),
            'budget': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter amount in ₹'}),
            'required_niche': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Tech, Fashion, Food'}),
        }