from django.db.models.signals import post_migrate, post_save
from django.dispatch import receiver
from django.conf import settings
from django.utils.text import slugify
from .models import ResumeTemplate, Resume

@receiver(post_migrate)
def create_default_resume_templates(sender, **kwargs):
    if sender.name == 'resume_builder':
        templates = [
            ('Classic', 'CLASSIC'),
            ('Modern', 'MODERN'),
            ('Creative', 'CREATIVE'),
            ('Technical', 'TECHNICAL'),
        ]
        for name, fmt in templates:
            ResumeTemplate.objects.get_or_create(
                name=name,
                format_type=fmt,
                defaults={'version': 1}
            )

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_default_resume(sender, instance, created, **kwargs):
    if created:
        base_slug = slugify(instance.username)
        unique_slug = base_slug
        counter = 1

        while Resume.objects.filter(slug=unique_slug).exists():
            unique_slug = f"{base_slug}-{counter}"
            counter += 1

        Resume.objects.create(
            user=instance,
            title="My First Resume",
            slug=unique_slug
        )
