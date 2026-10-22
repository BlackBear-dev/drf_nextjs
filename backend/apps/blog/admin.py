from django import forms
from django.contrib import admin
from django_ckeditor_5.widgets import CKEditor5Widget

from .models import Category, Heading, Post


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "title", "parent")
    search_fields = ("name", "slug", "title", "description")
    prepopulated_fields = {"slug": ("name",)}
    list_filter = ("parent",)
    ordering = ("name",)
    readonly_fields = (
        "created_at",
        "updated_at",
        "id",
    )


class PostAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditor5Widget(config_name="default"))

    class Meta:
        model = Post
        fields = "__all__"


class HeadingInline(admin.TabularInline):
    model = Heading
    extra = 1
    fields = ("title", "slug", "level", "order")
    prepopulated_fields = {"slug": ("title",)}
    ordering = ("order",)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm
    list_display = ("title", "slug", "status", "category", "created_at")
    search_fields = ("title", "slug", "description", "content", "keywords")
    prepopulated_fields = {"slug": ("title",)}
    list_filter = ("status", "category", "updated_at", "created_at")
    ordering = ("-created_at",)
    readonly_fields = (
        "created_at",
        "updated_at",
        "id",
    )
    fieldsets = (
        (
            "general information",
            {
                "fields": (
                    "title",
                    "description",
                    "content",
                    "thumbnail",
                    "keywords",
                    "slug",
                    "category",
                )
            },
        ),
        ("status", {"fields": ("status", "created_by")}),
        ("Timestamps", {"fields": ("created_at", "updated_at")}),
    )
    inlines = [HeadingInline]


# @admin.register(Heading)
# class HeadingAdmin(admin.ModelAdmin):
#     list_display = ("title", "post", "order")
#     search_fields = ("title", "post__title")
#     list_filter = ("level", "post")
#     ordering = ("order", "post")
#     prepopulated_fields = {"slug": ("title",)}
