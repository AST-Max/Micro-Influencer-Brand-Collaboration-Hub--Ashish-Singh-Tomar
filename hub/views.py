from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from .models import User, Profile, Campaign, Application
from .forms import InfluencerSignUpForm, BrandSignUpForm, ProfileForm, CampaignForm

# --- Home & Auth ---

def home(request):
    return render(request, 'hub/home.html')

def influencer_signup(request):
    if request.method == 'POST':
        form = InfluencerSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile_edit')
    else:
        form = InfluencerSignUpForm()
    return render(request, 'hub/signup.html', {'form': form})

def brand_signup(request):
    if request.method == 'POST':
        form = BrandSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = BrandSignUpForm()
    return render(request, 'hub/brand_signup.html', {'form': form})

# --- Profile Management ---

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'hub/profile_edit.html'

    def get_object(self):
        profile, created = Profile.objects.get_or_create(user=self.request.user)
        return profile

    def get_success_url(self):
        # Redirect to their specific dashboard after editing
        return reverse('dashboard')

@login_required
def profile_view(request):
    return render(request, 'hub/profile_view.html')

# --- THE SMART DASHBOARD (Fixed for Demo) ---

@login_required
def dashboard(request):
    user = request.user
    is_brand = getattr(user, 'is_brand', False)
    
    if is_brand:
        # Fetching all campaigns for the demo
        all_campaigns = Campaign.objects.all().order_by('-created_at')
        
        return render(request, 'hub/brand_dashboard.html', {
            'campaigns': all_campaigns,    # Name 1
            'my_campaigns': all_campaigns  # Name 2 (The safety net!)
        })
    else:
        # Influencer logic...
        my_apps = Application.objects.all().order_by('-applied_on')
        return render(request, 'hub/influencer_dashboard.html', {
            'applications': my_apps,
            'my_apps': my_apps # Safety net here too
        })
# --- Campaign & Gig Logic ---

class CampaignCreateView(LoginRequiredMixin, CreateView):
    model = Campaign
    form_class = CampaignForm
    template_name = 'hub/campaign_form.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        form.instance.brand = self.request.user
        messages.success(self.request, "Gig posted successfully!")
        return super().form_valid(form)

class CampaignFeedView(LoginRequiredMixin, ListView):
    model = Campaign
    template_name = 'hub/campaign_feed.html'
    context_object_name = 'campaigns'

    def get_queryset(self):
        return Campaign.objects.all().order_by('-created_at')

@login_required
def apply_to_campaign(request, pk):
    campaign = get_object_or_404(Campaign, pk=pk)
    
    if Application.objects.filter(influencer=request.user, campaign=campaign).exists():
        messages.warning(request, "You have already applied to this gig.")
        return redirect('campaign_feed')

    if request.method == 'POST':
        Application.objects.create(
            campaign=campaign,
            influencer=request.user,
            message=request.POST.get('message', '')
        )
        messages.success(request, f"Applied to {campaign.title}!")
        return redirect('dashboard')
        
    return render(request, 'hub/apply_form.html', {'campaign': campaign})

# --- Brand Management Tools ---

@login_required
def campaign_applicants(request, pk):
    campaign = get_object_or_404(Campaign, pk=pk)
    applicants = campaign.applications.all()
    return render(request, 'hub/applicants_list.html', {
        'campaign': campaign,
        'applicants': applicants,
    })

@login_required
def update_application_status(request, pk, status):
    application = get_object_or_404(Application, pk=pk)
    if status in ['accepted', 'declined']:
        application.status = status
        application.save()
    return redirect('campaign_applicants', pk=application.campaign.pk)
