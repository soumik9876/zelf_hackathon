from django.db import models

from core.models import BaseModel
from django.utils.translation import gettext_lazy as _

from social_content.managers.author_manager import AuthorManager


class AbstractBaseSocialModel(BaseModel):
    # The unique ID of the object in the 3rd party API platform
    hack_uid = models.PositiveIntegerField(verbose_name=_('HackAPI Unique ID'), unique=True)

    class Meta:
        abstract = True


class OriginDetails(models.Model):
    origin_platform = models.CharField(max_length=25, verbose_name=_('Origin platform'))
    origin_url = models.URLField(verbose_name=_('Origin URL'), blank=True)

    class Meta:
        verbose_name = _('Origin Details')

    def __str__(self):
        return f'{self.origin_platform}::{self.origin_url}'


class Context(models.Model):
    main_text = models.TextField(verbose_name=_('Main Text'), blank=True)
    token_count = models.PositiveIntegerField(verbose_name=_('Token count'), default=0)
    char_count = models.PositiveIntegerField(verbose_name=_('Character count'), default=0)
    tag_count = models.PositiveIntegerField(verbose_name=_('Tag count'), default=0)

    class Meta:
        verbose_name = _('Context')
        verbose_name_plural = _('Contexts')

    def __str__(self):
        return self.main_text


class Media(models.Model):
    urls = models.JSONField(verbose_name=_('Urls'), default=list)
    media_type = models.CharField(max_length=20, verbose_name=_('Media type'), default='IMAGE')

    class Meta:
        verbose_name = _('Media')
        verbose_name_plural = _('Medias')


class ContentStats(models.Model):
    likes = models.PositiveIntegerField(verbose_name=_('Likes'), default=0)
    views = models.PositiveIntegerField(verbose_name=_('Views'), default=0)
    comments = models.PositiveIntegerField(verbose_name=_('Comments'), default=0)

    class Meta:
        verbose_name = _('Content Stats')


class AuthorStats(models.Model):
    followers = models.PositiveIntegerField(verbose_name=_('Followers'), default=0)

    class Meta:
        verbose_name = _('Author Stats')


class AuthorInfo(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('Name'), blank=True)
    platform = models.CharField(max_length=100, verbose_name=_('Platform'), blank=True)

    class Meta:
        verbose_name = _('Author Info')


class Author(AbstractBaseSocialModel):
    info = models.OneToOneField(AuthorInfo, verbose_name=_('Info'), on_delete=models.SET_NULL, null=True)
    username = models.CharField(max_length=100, verbose_name=_('Username'))
    stats = models.OneToOneField(AuthorStats, verbose_name=_('Stats'), on_delete=models.SET_NULL, null=True)
    """
        Example for avatar JSON
        {
            "urls": [
                "https://nyc3.digitaloceanspaces.com/hellozelf/content/b0465689-8fd7-4845-8c3c-9752e0811643.jpg"
            ]
        }
    """
    avatar = models.JSONField(verbose_name=_('Avatar'), default=dict)
    """
        Example for texts JSON
        {
            "profile_text": "🍔 | Food Blogger 📸👨🏼\u200d⚖️ | Honest food ratings ⭐️📍 | Cairo, Egypt 🇪🇬📩 | DM for collabs 😍"
        }
    """
    texts = models.JSONField(verbose_name=_('Texts'), default=dict)
    objects = AuthorManager()

    class Meta:
        verbose_name = _('Author')
        verbose_name_plural = _('Authors')


class Content(AbstractBaseSocialModel):
    originally_created_at = models.DateTimeField(verbose_name=_('Originally created at'), null=True, blank=True)
    author = models.ForeignKey(Author, verbose_name=_('Author'), on_delete=models.SET_NULL, null=True)

    context = models.OneToOneField(Context, verbose_name=_('Context'), on_delete=models.SET_NULL, null=True)

    origin_details = models.OneToOneField(OriginDetails, verbose_name=_('Origin Details'), on_delete=models.SET_NULL,
                                          null=True)

    media = models.OneToOneField(Media, verbose_name=_('Media'), on_delete=models.SET_NULL, null=True)

    stats = models.OneToOneField(ContentStats, verbose_name=_('Content Stats'), on_delete=models.SET_NULL, null=True)

    # Custom manager
    from social_content.managers.content_manager import ContentManager
    objects = ContentManager()

    class Meta:
        verbose_name = _('Content')
        verbose_name_plural = _('Contents')

    def __str__(self):
        return self.hack_uid
