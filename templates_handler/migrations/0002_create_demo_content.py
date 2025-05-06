from django.db import migrations

def create_demo_content(apps, schema_editor):
    ContentContainer = apps.get_model('templates_handler', 'ContentContainer')
    ContentItem = apps.get_model('templates_handler', 'ContentItem')
    TeamMember = apps.get_model('templates_handler', 'TeamMember')
    Testimonial = apps.get_model('templates_handler', 'Testimonial')
    
    # Only create demo content if no containers exist yet
    if ContentContainer.objects.count() == 0:
        # 1. Landing Page Containers
        # Hero Section
        hero = ContentContainer.objects.create(
            name="Main Hero Section",
            container_type="image_text",
            page_location="landing",
            order=1,
            is_active=True
        )
        ContentItem.objects.create(
            container=hero,
            title="Welcome to Our Website",
            content="<p>This is a sample hero section created automatically. You can edit or delete this content through the admin panel.</p>",
            image_position="right",
            button_text="Get Started",
            button_url="#services",
            order=1
        )
        
        # Features Section
        features = ContentContainer.objects.create(
            name="Features Section",
            container_type="card",
            page_location="landing",
            order=2,
            is_active=True
        )
        ContentItem.objects.create(
            container=features,
            title="Our Awesome Features",
            order=0  # This will be the section title
        )
        ContentItem.objects.create(
            container=features,
            title="Easy to Use",
            content="Our platform is designed with simplicity in mind, making it accessible to everyone.",
            order=1
        )
        ContentItem.objects.create(
            container=features,
            title="Fully Responsive",
            content="Looks great on all devices from smartphones to desktop computers.",
            order=2
        )
        ContentItem.objects.create(
            container=features,
            title="Customizable",
            content="Tailor the system to your specific needs with our flexible options.",
            order=3
        )
        
        # 2. About Page Containers
        # About Us Section
        about = ContentContainer.objects.create(
            name="About Us Section",
            container_type="plain_text",
            page_location="about",
            order=1,
            is_active=True
        )
        ContentItem.objects.create(
            container=about,
            title="About Our Company",
            content="<p>This is a sample about us section. You can replace this with your actual company information.</p><p>We're a team of passionate individuals dedicated to creating amazing digital experiences.</p>",
            order=1
        )
        
        # Team Section
        team = ContentContainer.objects.create(
            name="Our Team",
            container_type="team",
            page_location="about",
            order=2,
            is_active=True
        )
        ContentItem.objects.create(
            container=team,
            title="Meet Our Team",
            order=0
        )
        TeamMember.objects.create(
            container=team,
            name="John Doe",
            position="CEO & Founder",
            bio="John founded the company in 2010 with a vision to revolutionize the industry.",
            order=1,
            email="john@example.com",
            social_media={'twitter': 'https://twitter.com/johndoe', 'linkedin': 'https://linkedin.com/in/johndoe'}
        )
        TeamMember.objects.create(
            container=team,
            name="Jane Smith",
            position="Marketing Director",
            bio="Jane leads our marketing efforts with over 10 years of experience.",
            order=2,
            email="jane@example.com",
            social_media={'twitter': 'https://twitter.com/janesmith', 'linkedin': 'https://linkedin.com/in/janesmith'}
        )
        
        # 3. Contact Page Containers
        contact = ContentContainer.objects.create(
            name="Contact Information",
            container_type="plain_text",
            page_location="contact",
            order=1,
            is_active=True
        )
        ContentItem.objects.create(
            container=contact,
            title="Get In Touch",
            content="<p>Email: info@example.com</p><p>Phone: (123) 456-7890</p><p>Address: 123 Main St, Anytown, USA</p>",
            order=1
        )
        
        contact_form = ContentContainer.objects.create(
            name="Contact Form",
            container_type="contact_form",
            page_location="contact",
            order=2,
            is_active=True
        )
        ContentItem.objects.create(
            container=contact_form,
            title="Send Us a Message",
            content="<p>Have questions? Fill out the form below and we'll get back to you as soon as possible.</p>",
            order=1
        )
        
        # Testimonials (shown on landing page)
        testimonials = ContentContainer.objects.create(
            name="Customer Testimonials",
            container_type="testimonial",
            page_location="landing",
            order=3,
            is_active=True
        )
        ContentItem.objects.create(
            container=testimonials,
            title="What Our Clients Say",
            order=0
        )
        Testimonial.objects.create(
            container=testimonials,
            author="Sarah Johnson",
            position="Marketing Manager at ABC Corp",
            content="This platform has transformed how we manage our content. Highly recommended!",
            rating=5,
            order=1
        )
        Testimonial.objects.create(
            container=testimonials,
            author="Michael Brown",
            position="CTO at XYZ Inc",
            content="The flexibility and ease of use are unmatched. Our team adopted it immediately.",
            rating=4,
            order=2
        )

def delete_demo_content(apps, schema_editor):
    ContentContainer = apps.get_model('templates_handler', 'ContentContainer')
    ContentContainer.objects.all().delete()

class Migration(migrations.Migration):

    dependencies = [
        ('templates_handler', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_demo_content, delete_demo_content),
    ]
