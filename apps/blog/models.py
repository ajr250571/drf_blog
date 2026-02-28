import uuid
from django.db import models
from django.utils import timezone
from django.utils.text import slugify

def blog_post_directory_path(instance, filename):
    return 'blog_posts/{0}/{1}'.format(instance.title, filename)

def blog_category_directory_path(instance, filename):
    return 'blog_categories/{0}/{1}'.format(instance.title, filename)


class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    parent = models.ForeignKey('self', blank=True, null=True, related_name='children', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    thumbnail = models.ImageField(upload_to=blog_category_directory_path, null=True, blank=True)
    slug = models.SlugField(max_length=128, unique=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

class Post(models.Model):
    class PostObjects(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(status='published')

    STATUS_OPTIONS = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=128)
    description = models.CharField(max_length=255)
    content = models.TextField()
    thumbnail = models.ImageField(upload_to=blog_post_directory_path, null=True, blank=True)
    keywords = models.CharField(max_length=128)
    slug = models.SlugField(max_length=128, unique=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    status = models.CharField(max_length=10, choices=STATUS_OPTIONS, default='draft')

    category = models.ForeignKey(Category, on_delete=models.PROTECT)

    objects = models.Manager()
    published = PostObjects()

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.title

class Heading(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='headings')
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    level = models.IntegerField(choices=[(1, 'h1'), (2, 'h2'), (3, 'h3'), (4, 'h4'), (5, 'h5'), (6, 'h6')], default=1)
    order = models.PositiveIntegerField()
    
    class Meta:
        ordering = ('order',)

    def __str__(self):
        return self.title

    def save(self):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save()