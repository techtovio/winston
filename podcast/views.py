from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Podcast, PodcastCategory, SubscriptionPlan, Subscription
from django.utils import timezone

def podcast_list(request):
    categories = PodcastCategory.objects.all()
    category_id = request.GET.get('category')
    
    podcasts = Podcast.objects.filter(publish_date__lte=timezone.now()).order_by('-publish_date')
    
    if category_id:
        podcasts = podcasts.filter(categories__id=category_id)
    
    # Filter based on user access
    filtered_podcasts = []
    for podcast in podcasts:
        if podcast.user_can_access(request.user):
            filtered_podcasts.append(podcast)
    
    paginator = Paginator(filtered_podcasts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'categories': categories,
        'selected_category': int(category_id) if category_id else None,
        'has_subscription': has_active_subscription(request.user) if request.user.is_authenticated else False,
    }
    return render(request, 'podcast/podcast.html', context)

def podcast_detail(request, pk):
    podcast = get_object_or_404(Podcast, pk=pk)
    
    if not podcast.user_can_access(request.user):
        if request.user.is_authenticated:
            messages.warning(request, "You need an active subscription to access this podcast")
            return redirect('subscription_plans')
        else:
            messages.warning(request, "Please login and subscribe to access this podcast")
            return redirect('login')
    
    # Get related podcasts (same category, excluding current)
    related_podcasts = Podcast.objects.filter(
        categories__in=podcast.categories.all(),
        publish_date__lte=timezone.now()
    ).exclude(pk=podcast.pk).distinct()[:4]
    
    context = {
        'podcast': podcast,
        'related_podcasts': related_podcasts,
    }
    return render(request, 'podcast/podcast_detail.html', context)

@login_required
def subscription_plans(request):
    plans = SubscriptionPlan.objects.filter(is_active=True)
    
    # Filter plans based on user type
    available_plans = []
    for plan in plans:
        allowed_types = [t.strip() for t in plan.allowed_user_types.split(',')]
        if request.user.user_type in allowed_types:
            available_plans.append(plan)
    
    # Check if user already has active subscription
    has_active = Subscription.objects.filter(
        user=request.user,
        is_active=True,
        valid_until__gte=timezone.now()
    ).exists()
    
    context = {
        'plans': available_plans,
        'has_active_subscription': has_active,
        'user_type': request.user.user_type,
    }
    return render(request, 'podcast/subscription_plans.html', context)

def has_active_subscription(user):
    if not user.is_authenticated:
        return False
    return Subscription.objects.filter(
        user=user,
        is_active=True,
        valid_until__gte=timezone.now()
    ).exists()