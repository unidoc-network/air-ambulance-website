from django.db import models
from autoslug.fields import AutoSlugField
from PIL import Image
import io
from django.core.files.base import ContentFile

# Create your models here.

class ImageCompressMixin:
    """
    Reusable mixin to compress ImageFields when saving models.
    """

    def compress(self, image_field):
        if not image_field:
            return image_field

        img = Image.open(image_field)

        # Convert to RGB if needed
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")

        img_io = io.BytesIO()

        # Save with good quality and compression
        img.save(img_io, format='JPEG', optimize=True, quality=80)

        new_image = ContentFile(img_io.getvalue(), image_field.name)

        return new_image
    
class BaseModel(models.Model):
    """
    Abstract base model that includes common fields for all models:
    - is_active: Marks if the object is active.
    - created_at: Timestamp when the object was created.
    - updated_at: Timestamp when the object was last updated.
    """
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

# Removed Popup, Gallery models


# Removed Category, Menu, and Tag models as they are no longer needed for the medical transport theme.


# Removed Testimonials model



class ContactForm(BaseModel):
    """
    Model to store messages sent from the contact form.
    """
    name = models.CharField(max_length=100, null=True)
    email = models.EmailField(null=True)
    country_code = models.CharField(max_length=10, null=True, blank=True)
    phone = models.TextField(null=True, blank=True)
    service = models.CharField(max_length=255, null=True, blank=True)
    message = models.TextField(null=True)
    country = models.CharField(max_length=100, default='Website', null=True, blank=True)

    @property
    def full_phone(self):
        if self.country_code and self.phone:
            return f"{self.country_code} {self.phone}"
        return self.phone or "-"

# Removed Team model


class BlogCategory(BaseModel):
    """
    Model for blog categories.
    """
    name = models.CharField(max_length=255, null=True, blank=True)
    name_ar = models.CharField(max_length=255, null=True, blank=True, verbose_name="Arabic Name")
    slug = AutoSlugField(populate_from="name", null=True, blank=True, unique=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name if self.name else f"Category {self.id}"

class Blogs(BaseModel, ImageCompressMixin):
    """
    Model for news and stories.
    """
    category = models.ForeignKey(BlogCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='blogs')
    title = models.TextField(null=True, blank=True)
    title_ar = models.TextField(null=True, blank=True, verbose_name="Arabic Title")
    date = models.DateField(null=True, blank=True)
    image = models.ImageField(upload_to='Blogs', null=True, blank=True)
    content = models.TextField(null=True, blank=True)  # English content, used with Summernote
    content_ar = models.TextField(null=True, blank=True, verbose_name="Arabic Content")  # Arabic content, used with Summernote
    time_to_read = models.CharField(max_length=50, null=True, blank=True, verbose_name="Time to Read (EN)")  # Optional
    time_to_read_ar = models.CharField(max_length=50, null=True, blank=True, verbose_name="Time to Read (AR)")  # Optional
    tag = models.CharField(max_length=100, null=True, blank=True)  # e.g. "Food Story"
    slug = AutoSlugField(populate_from="title", null=True, blank=True, unique=True)

    class Meta:
        verbose_name = "News & Story"
        verbose_name_plural = "News & Stories"

    def __str__(self):
        return self.title if self.title else f"News {self.id}"

    def save(self, *args, **kwargs):
        try:
            old = Blogs.objects.get(id=self.id)
            old_image = old.image
        except Blogs.DoesNotExist:
            old_image = None

        super().save(*args, **kwargs)


# Removed GlobalStats model


class Career(BaseModel):
    """
    Model for job career listings.
    """
    # English fields
    title = models.CharField(max_length=255, null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    listing_description = models.TextField(null=True, blank=True, verbose_name="Listing Description (EN)")  # Short description shown on listing/card
    description = models.TextField(null=True, blank=True, verbose_name="Detail Description (EN)")  # Full detail page content (Summernote)

    # Arabic fields
    title_ar = models.CharField(max_length=255, null=True, blank=True, verbose_name="Job Title (AR)")
    location_ar = models.CharField(max_length=255, null=True, blank=True, verbose_name="Location (AR)")
    listing_description_ar = models.TextField(null=True, blank=True, verbose_name="Listing Description (AR)")  # Short description for listing (AR)
    description_ar = models.TextField(null=True, blank=True, verbose_name="Detail Description (AR)")  # Full detail page content (AR, Summernote)

    slug = AutoSlugField(populate_from="title", null=True, blank=True, unique=True)

    class Meta:
        verbose_name = "Career"
        verbose_name_plural = "Careers"

    def __str__(self):
        return self.title if self.title else f"Career {self.id}"

class CareerApplication(BaseModel):
    """
    Model for job applications.
    """
    career = models.ForeignKey(Career, on_delete=models.CASCADE, related_name='applications')
    name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    country_code = models.CharField(max_length=10, null=True, blank=True)
    phone = models.CharField(max_length=50, null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    resume = models.FileField(upload_to='Resumes/', null=True, blank=True)

    class Meta:
        verbose_name = "Career Application"
        verbose_name_plural = "Career Applications"

    def __str__(self):
        return f"{self.name} - {self.career.title}"

    @property
    def full_phone(self):
        if self.country_code and self.phone:
            return f"{self.country_code} {self.phone}"
        return self.phone or "-"


