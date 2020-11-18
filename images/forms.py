from django import forms
from .models import Image
from urllib import request
from django.core.files.base import ContentFile
from django.utils.text import slugify


class ImageCreationForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['title', 'url', 'description',]
        widgets ={
            'url':forms.HiddenInput,
        }

    def clean_url(self):
        url = self.cleaned_data['url']
        #Check the URL has a valid extension
        valid_extensions = ['jpg', 'jpeg', 'png']
        has_extension = any([url.endswith(e) for e in valid_extensions])#url.split('.', 1)[1].lower()
        if not has_extension:
            raise_form.ValidationError('The given URL soen not match valid image extensions')

        #Check the image exists on the server
        #
        return url

    def save(self, force_insert = False, force_update=False, commit=True):
        image = super().save(commit=False)
        image_url = self.cleaned_data['url']
        name = slugify(image.title)
        extension = image_url.rsplit('.', 1)[1].lower()
        image_name = f'{name}.{extension}'

        #download image from the given url
        print('Going to get: ', image_url)
        # try:
        response = request.urlopen(image_url)
        # except:
            # 'Enter a valid Image URL'
        image.image.save(image_name, ContentFile(response.read()), save=False)
        if commit:
            image.save()
        return image
