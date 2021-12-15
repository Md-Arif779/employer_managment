from django.db import models
from PIL import Image
from multiselectfield import MultiSelectField
from django.contrib.auth.models import User
from django.db.models.fields import CharField
# Create your models here

class Post(models.Model):
    CATEGORY=(
        ('Driver','Driver'),
        ('Nures','Nures'),
        ('Work_maid','Work_maid'),
    )
    LANGUAGE=(
        ('Bangla','Bangla'),
        ('English','English'),
        ('Hindi','Hindi'),
        ('Arabir','Arabic'),
    )
    user=models.OneToOneField(User,on_delete=models.CASCADE, blank=True, null=True)
    Name=models.CharField(max_length=100)
    Phone=models.CharField(max_length=17)
    Email=models.EmailField()
    NID=models.CharField(max_length=25,)
    Present_Adress=models.TextField()
    Permanent_Adress=models.TextField()
    Available=models.BooleanField()
    Category=models.CharField(max_length=100,choices= CATEGORY,default=1)
    language=MultiSelectField(max_length=100, max_choices=4,choices=LANGUAGE,default='Bangla')
    Details=models.TextField()
    image=models.ImageField(default='default.jpg',upload_to='media/images')
    DateTime=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.Name
    
    def save(self):
        super().save()
        
        img = Image.open(self.image.path)
        
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
    
    
    # def ProperCase(self):
    #     return self.Name.name()
    # def details_short(self):
    #     details_words=self.details.split(' ')
    #     if len(details_words)>10:
    #         return ' '.join(details_words[:10])+ "...."
    #     else:
    #         return self.details
    
    
class Comment(models.Model): 
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.TextField()
    parent = models.ForeignKey('self',on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.user.username + ": " + self.text[0:15]