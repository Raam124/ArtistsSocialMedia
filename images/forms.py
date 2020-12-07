from django import forms
from images.models import Pictures
from taggit.forms import TagWidget


class CreatePostForm(forms.ModelForm):
    
    class Meta:
        model = Pictures
        fields = ('title','image','tags','description','category')
        widgets = {
            'tags': TagWidget(),
        }
        

        

class UpdatePostForm(forms.ModelForm):

    class Meta: 
        model = Pictures
        fields = ('title','image','description','category')
        widgets = {
            'tags': TagWidget(),
        }

    def save(self, commit=True):
        image_post = self.instance
        image_post.title = self.cleaned_data['title']
        image_post.description = self.cleaned_data['description']
        # image_post.tags = self.cleaned_data['tags']
        image_post.category = self.cleaned_data['category']
        
        if self.cleaned_data['image']:
            image_post.image = self.cleaned_data['image']

        if commit:
            image_post.save()
            image_post.save_m2m()
        return image_post

    # def save_m2m(self, commit=False):
    #     tag_post = self.instance
     
    #     if self.cleaned_data['tags']:
    #         tag_post.image = self.cleaned_data['tags']
            
    #     if commit:
    #         tag_post.save()
    #         tag_post.save_m2m()
    #     return tag_post



