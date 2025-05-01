from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.urls import reverse
from django.utils import timezone
from django.conf import settings
from django.core.mail import send_mail
from .models import Ebook, EbookCategory, EbookPurchase
from .forms import GuestPurchaseForm, AccountPurchaseForm
import uuid
from datetime import timedelta

def ebook_list(request):
    categories = EbookCategory.objects.all()
    category_id = request.GET.get('category')
    featured = request.GET.get('featured')
    
    ebooks = Ebook.objects.filter(is_active=True).order_by('-is_featured', '-publish_date')
    
    if category_id:
        ebooks = ebooks.filter(categories__id=category_id)
    if featured:
        ebooks = ebooks.filter(is_featured=True)
    
    paginator = Paginator(ebooks, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'categories': categories,
        'selected_category': int(category_id) if category_id else None,
        'show_featured': featured is not None,
    }
    return render(request, 'ebooks/ebook_list.html', context)

def ebook_detail(request, slug):
    ebook = get_object_or_404(Ebook, slug=slug, is_active=True)
    related_ebooks = Ebook.objects.filter(
        categories__in=ebook.categories.all(),
        is_active=True
    ).exclude(pk=ebook.pk).distinct()[:4]
    
    context = {
        'ebook': ebook,
        'related_ebooks': related_ebooks,
    }
    return render(request, 'ebooks/ebook_detail.html', context)

def purchase_options(request, slug):
    ebook = get_object_or_404(Ebook, slug=slug, is_active=True)
    
    if request.user.is_authenticated:
        # Check if user already purchased this ebook
        if EbookPurchase.objects.filter(ebook=ebook, user=request.user, is_paid=True).exists():
            messages.info(request, "You've already purchased this eBook!")
            return redirect('ebook_detail', slug=slug)
        
        if request.method == 'POST':
            form = AccountPurchaseForm(request.POST)
            if form.is_valid():
                # In a real implementation, this would process payment
                # For now, we'll simulate successful payment
                purchase = EbookPurchase.objects.create(
                    ebook=ebook,
                    user=request.user,
                    email=request.user.email,
                    amount_paid=ebook.price,
                    is_paid=True,
                    download_expiry=timezone.now() + timedelta(days=30)
                )
                
                # Send download link
                send_download_link(purchase)
                
                messages.success(request, "Purchase successful! Download link has been sent to your email.")
                return redirect('ebook_detail', slug=slug)
        else:
            form = AccountPurchaseForm()
    else:
        if request.method == 'POST':
            form = GuestPurchaseForm(request.POST)
            if form.is_valid():
                # Simulate payment processing
                purchase = EbookPurchase.objects.create(
                    ebook=ebook,
                    email=form.cleaned_data['email'],
                    amount_paid=ebook.price,
                    is_paid=True,
                    download_expiry=timezone.now() + timedelta(days=30)
                )
                
                # Send download link
                send_download_link(purchase)
                
                messages.success(request, "Purchase successful! Download link has been sent to your email.")
                return redirect('ebook_detail', slug=slug)
        else:
            form = GuestPurchaseForm()
    
    context = {
        'ebook': ebook,
        'form': form,
        'is_authenticated': request.user.is_authenticated,
    }
    return render(request, 'ebooks/purchase_options.html', context)

def send_download_link(purchase):
    # In a real implementation, this would send an actual email
    # For simulation, we'll just print to console
    download_url = f"https://yourdomain.com/download/{purchase.id}/"
    message = f"""
    Thank you for purchasing {purchase.ebook.title}!
    
    Your download link: {download_url}
    This link will expire on {purchase.download_expiry.strftime('%B %d, %Y')}.
    
    Happy reading!
    """
    
    print(f"Email sent to {purchase.email} with download link: {download_url}")
    # Uncomment to actually send emails in production
    # send_mail(
    #     f"Your eBook Download: {purchase.ebook.title}",
    #     message,
    #     settings.DEFAULT_FROM_EMAIL,
    #     [purchase.email],
    #     fail_silently=False,
    # )