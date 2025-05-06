# templates_handler/templatetags/content_containers.py
from django import template
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from ..models import ContentContainer

register = template.Library()

@register.simple_tag(takes_context=True)
def render_content_container(context, page_location):
    request = context.get('request')
    containers = ContentContainer.objects.filter(
        page_location__in=[page_location, 'all'],
        is_active=True
    ).prefetch_related('items', 'team_members', 'testimonials')
    
    output = []
    for container in containers:
        template_name = f"templates_handler/containers/{container.container_type}.html"
        try:
            rendered = render_to_string(template_name, {
                'container': container,
                'request': request,
            }, request=request)
            output.append(rendered)
        except template.TemplateDoesNotExist:
            continue
    
    return mark_safe(''.join(output))  # This is crucial
