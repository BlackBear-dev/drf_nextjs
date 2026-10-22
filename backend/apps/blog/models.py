from uuid import uuid4

from django.db import models
from django.utils.text import slugify
from django_ckeditor_5.fields import CKEditor5Field


def blog_thumbnail_directory(instance, filename):
    return f"blog_posts/{instance.slug}/{filename}"


def category_thumbnail_directory(instance, filename):
    return f"blog_categories/{instance.slug}/{filename}"


class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    parent = models.ForeignKey(
        "self",
        related_name="children",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    name = models.CharField(max_length=255, unique=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    thumbnail = models.ImageField(
        upload_to=category_thumbnail_directory, null=True, blank=True
    )

    slug = models.SlugField(unique=True)

    created_by = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Post(models.Model):

    class PostObjects(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(status="published")

    status_options = [("draft", "Draft"), ("published", "Published")]

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    title = models.CharField(max_length=128)
    description = models.CharField(max_length=256)
    content = CKEditor5Field("content", config_name="default")
    thumbnail = models.ImageField(
        upload_to=blog_thumbnail_directory, null=True, blank=True
    )

    slug = models.SlugField(unique=True)
    keywords = models.CharField(max_length=200, blank=True)

    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, related_name="posts"
    )

    status = models.CharField(max_length=10, choices=status_options, default="draft")
    created_by = models.ForeignKey("auth.User", on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    objects = models.Manager()  # default manager
    postObjects = PostObjects()  # custom manager

    class Meta:
        ordering = ["status", "-created_at"]


class Heading(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    post = models.ForeignKey(Post, on_delete=models.PROTECT, related_name="headings")
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    level = models.PositiveSmallIntegerField(
        choices=[(1, "H1"), (2, "H2"), (3, "H3"), (4, "H4"), (5, "H5"), (6, "H6")],
    )
    order = models.PositiveSmallIntegerField()

    class Meta:
        unique_together = ("post", "slug")
        ordering = ["order"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
