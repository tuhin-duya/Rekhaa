from django.conf import settings
from django.db import models
from django.core.validators import FileExtensionValidator


class ArtistModel(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    photo = models.ImageField(upload_to="artist/", blank=True)
    video = models.FileField(
            upload_to="paintings/videos/",
            blank=True,                                                  
            validators=[FileExtensionValidator(["mp4", "webm","mov"])],        # only these file types
        )
    bio = models.TextField()
    statement = models.TextField(blank=True)
    inspirations = models.TextField(blank=True)
    themes = models.CharField(max_length=300, blank=True, help_text="Comma separated")
    mediums = models.CharField(max_length=300, blank=True, help_text="Comma separated")

    @property
    def name(self):
        return self.user.get_full_name() or self.user.username

    def theme_list(self):
        return [t.strip() for t in self.themes.split(",") if t.strip()]

    def medium_list(self):
        return [m.strip() for m in self.mediums.split(",") if m.strip()]

    def __str__(self):
        return self.name

class Milestones(models.Model):
    artist = models.ForeignKey(ArtistModel, on_delete=models.CASCADE, related_name = "milestones" )
    year = models.PositiveIntegerField()
    title = models.CharField(max_length=150)
    note = models.CharField(max_length = 250, blank = True)
    
    class Meta:
        ordering = ["year"]
    
    def __str__(self):
        return f"{self.year} - {self.title}"
    
class Category(models.Model):
    artist = models.ForeignKey(ArtistModel,on_delete=models.CASCADE, related_name="categories" )
    title = models.CharField(max_length=150)
    desc = models.TextField(max_length=350,blank=True)
    cover = models.ImageField(upload_to="categories/", blank=True)
    
    def __str__(self):
        return self.title

class Painting(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="paintings")
    title = models.CharField(max_length=150)
    desc = models.TextField(max_length=350,blank=True)
    image = models.ImageField(upload_to="paintings/")
    video = models.FileField(
        upload_to="paintings/videos/",
        blank=True,                                                  
        validators=[FileExtensionValidator(["mp4", "webm","mov"])],        # only these file types
    )
    
    def __str__(self):
        return self.title
