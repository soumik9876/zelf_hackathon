from django.db import models
from django.utils.translation import gettext as _

class BaseModel(models.Model):
    """
        Base model for inheriting common fields
    """
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Constant(BaseModel):
    key = models.CharField(max_length=255, verbose_name=_('Key'), unique=True)
    value = models.TextField(verbose_name=_('Value'))

    def __str__(self):
        return self.key