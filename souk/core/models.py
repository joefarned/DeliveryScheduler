import os
import uuid

from django.db import models
from django.conf import settings


def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('item_imgs', filename)


class Item(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='+')
    possessor = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='+')

    name = models.CharField(blank=False, max_length=250)
    desc = models.TextField(blank=True)
    picture = models.ImageField(blank=True, upload_to=get_file_path)

    class Meta:
        verbose_name = "Item"
        verbose_name_plural = "Items"

    def filename(self):
        return os.path.basename(self.picture.name)

    def __str__(self):
        return unicode(self.name)


class Nest(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    code = models.CharField(blank=False, max_length=250)
    access_token = models.TextField(blank=False)
    updated = models.DateTimeField(auto_now=True)
    home = models.CharField(blank=True, max_length=15)

    class Meta:
        verbose_name = "Nest"
        verbose_name_plural = "Nests"

    def __str__(self):
        return unicode(self.user)


class Request(models.Model):
    requestor = models.ForeignKey(settings.AUTH_USER_MODEL)
    item = models.ForeignKey(Item, related_name='requests', blank=True, null=True)
    craig = models.ForeignKey("CraigPost", blank=True, null=True)
    address = models.CharField(blank=True, max_length=450)
    added = models.DateTimeField(auto_now_add=True)

    accepted = models.BooleanField(default=False)
    in_progress = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)

    cost_delivery = models.IntegerField(default=0)
    delivery_id = models.CharField(blank=True, max_length=50)
    delivery_estimate = models.DateTimeField(blank=True, null=True)
    pickup_estimate = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = "Request"
        verbose_name_plural = "Requests"

    def __str__(self):
        return unicode(self.item) + unicode(self.requestor)


class Profile(models.Model):
    address = models.TextField(blank=False)
    phone_number = models.CharField(blank=False, max_length=50)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, related_name='profile')
    balance = models.DecimalField(default=0, max_digits=5, decimal_places=2)

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"

    def __str__(self):
        return unicode(self.address)


class CraigPost(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    url = models.URLField()
    title = models.CharField(blank=False, max_length=250)
    email = models.EmailField()
    added = models.DateTimeField(auto_now_add=True)

    price = models.IntegerField(default=0)
    address = models.CharField(blank=True, max_length=450)
    completed = models.BooleanField(default=True)

    class Meta:
        verbose_name = "CraigPost"
        verbose_name_plural = "CraigPosts"

    def __str__(self):
        return unicode(self.title)


class Message(models.Model):
    post = models.ForeignKey(CraigPost, blank=True, null=True)
    text = models.TextField()
    added = models.DateTimeField(auto_now_add=True)
    from_us = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Message"
        verbose_name_plural = "Messages"

    def __str__(self):
        return unicode(self.text)

