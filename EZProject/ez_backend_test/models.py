from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.template.defaultfilters import slugify
import os
from django.utils.translation import gettext as _
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator


class CustomUser(AbstractUser):
    STATUS = (
        ('regular', 'regular'),
        ('subscriber', 'subscriber'),
        ('moderator', 'moderator'),
    )

    email = models.EmailField(unique=True)
    status = models.CharField(max_length=100, choices=STATUS, default='regular')
    is_active = models.BooleanField(default=False)
    username = models.CharField(max_length=30, unique=True, null=True, blank=True)

    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        help_text=_(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_name='customuser_set',  
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name='customuser_set',  
    )


class Files(models.Model):
    allowed_file_types = ['pdf', 'ppt', 'docx', 'xlsx']

    file = models.FileField(
        upload_to='store/files/',
        validators=[FileExtensionValidator(allowed_extensions=allowed_file_types)],
        default='store/files/default_file.pdf'
    )

    def __str__(self):
        return self.file.name
