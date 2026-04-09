from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    # Boolean flags to determine the user type
    is_brand = models.BooleanField(default=False)
    is_influencer = models.BooleanField(default=False)

    def __str__(self):
        return self.username
    




class Profile(models.Model):
    # Links the profile to the Custom User
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    # Common fields
    bio = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True) # e.g., "Lucknow"
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    
    # Influencer specific fields
    niche = models.CharField(max_length=50, blank=True) # e.g., "Lifestyle", "Tech"
    instagram_handle = models.CharField(max_length=100, blank=True)
    follower_count = models.PositiveIntegerField(default=0)

    # Brand specific fields
    company_name = models.CharField(max_length=150, blank=True)
    website = models.URLField(blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"


class Campaign(models.Model):
    # A campaign belongs to a Brand (User)
    brand = models.ForeignKey(User, on_delete=models.CASCADE, related_name='campaigns')
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Requirements for the influencer
    required_niche = models.CharField(max_length=50)
    min_followers = models.PositiveIntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
  
    def calculate_match(self, influencer_profile):
        """
        Calculates a compatibility score between 0-100.
        60% weightage to Niche, 40% to Follower Count.
        """
        score = 0
        # Match by Niche (Case-insensitive)
        if self.required_niche.lower() == influencer_profile.niche.lower():
            score += 60
        
        # Match by Follower Count
        if influencer_profile.follower_count >= self.min_followers:
            score += 40
        elif self.min_followers > 0: # Avoid division by zero
            # Partial points for being close
            percentage = (influencer_profile.follower_count / self.min_followers) * 40
            score += int(percentage)
            
        return score

    def __str__(self):
        return self.title

class Application(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('declined', 'Declined'),
    )

    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='applications')
    influencer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications_submitted')
    
    message = models.TextField(help_text="Pitch to the brand", blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    applied_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        # This prevents the SAME influencer from applying to the SAME campaign twice
        unique_together = ('campaign', 'influencer')

    def __str__(self):
        return f"{self.influencer.username} -> {self.campaign.title}"