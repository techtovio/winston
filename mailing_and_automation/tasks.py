# tasks.py
from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone
from .models import DripCampaign, SentEmail
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

@shared_task
def send_drip_campaign_emails():
    now = timezone.now()
    active_campaigns = DripCampaign.objects.filter(
        is_active=True,
        start_date__lte=now
    ).exclude(
        end_date__lt=now
    )
    
    for campaign in active_campaigns:
        # Check if it's time to send based on frequency
        should_send = False
        
        if campaign.frequency == 'once':
            if not campaign.last_sent:
                should_send = True
        elif campaign.frequency == 'daily':
            if not campaign.last_sent or (now - campaign.last_sent).days >= 1:
                should_send = True
        elif campaign.frequency == 'weekly':
            if not campaign.last_sent or (now - campaign.last_sent).days >= 7:
                should_send = True
        elif campaign.frequency == 'monthly':
            if not campaign.last_sent or (now - campaign.last_sent).days >= 30:
                should_send = True
        
        if should_send:
            try:
                recipients = campaign.recipient_group.get_recipients()
                template = campaign.template
                
                for recipient in recipients:
                    # Render email content
                    context = {
                        'recipient': recipient,
                        'custom_message': campaign.custom_message,
                        'campaign': campaign,
                    }
                    
                    subject = template.subject
                    html_content = template.content
                    if campaign.custom_message:
                        html_content += f"<p>{campaign.custom_message}</p>"
                    
                    # Send email
                    send_mail(
                        subject=subject,
                        message=html_content,  # For plain text fallback
                        html_message=html_content,
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[recipient],
                        fail_silently=False,
                    )
                    
                    # Record sent email
                    SentEmail.objects.create(
                        campaign=campaign,
                        recipient=recipient,
                        subject=subject,
                        content=html_content
                    )
                
                # Update campaign last_sent
                campaign.last_sent = now
                campaign.save()
                
                logger.info(f"Successfully sent campaign '{campaign.name}' to {len(recipients)} recipients")
                
            except Exception as e:
                logger.error(f"Error sending campaign '{campaign.name}': {str(e)}")
                continue