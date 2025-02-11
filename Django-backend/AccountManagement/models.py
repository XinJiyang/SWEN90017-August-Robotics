from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import Group, AbstractUser, Permission

class Account(AbstractUser):
    ADMIN = 'admin'
    MANAGER = 'manager'
    VIEWER = 'viewer'

    PRIVILEGE_CHOICES = [
        (ADMIN, 'admin'),
        (MANAGER, 'manager'),
        (VIEWER, 'viewer'),
    ]

    privilege = models.CharField(choices=PRIVILEGE_CHOICES, default=VIEWER)
    email = models.EmailField(verbose_name='user_email', max_length=32, blank=True, null=True)

    groups = models.ManyToManyField(
        Group,
        verbose_name=('groups'),
        blank=True,
        help_text=(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_name="account_groups",
        related_query_name="account",
    )
    
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=('user permissions'),
        blank=True,
        help_text=('Specific permissions for this user.'),
        related_name="account_user_permissions",
        related_query_name="account",
    )

    def to_dict(self):
        return {'username': self.username, 'privilege': self.privilege}
    
    def save(self, *args, **kwargs):
        super(Account, self).save(*args, **kwargs)
        if self.privilege == self.ADMIN:
            self.groups.add(Group.objects.get(name=self.ADMIN))
        elif self.privilege == self.MANAGER:
            self.groups.add(Group.objects.get(name=self.MANAGER))
        elif self.privilege == self.VIEWER:
            self.groups.add(Group.objects.get(name=self.VIEWER))
        return self
    
    class Meta:
        db_table = "accounts"

    
    
