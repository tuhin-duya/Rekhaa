from django.contrib import admin
from .models import ArtistModel,Milestones,Category,Painting

# Register your models here.
class MilestoneAdmin(admin.TabularInline):
    model = Milestones
    extra = 1

class CategoryInline(admin.TabularInline):
    model = Category
    extra = 1

class ArtistModelAdmin(admin.ModelAdmin):
    inlines = [MilestoneAdmin , CategoryInline]

admin.site.register(ArtistModel,ArtistModelAdmin)

class PaintingInline(admin.TabularInline):
    model = Painting
    extra = 1

class CategoryAdmin(admin.ModelAdmin):
    inlines = [PaintingInline]
    
admin.site.register(Category,CategoryAdmin)
