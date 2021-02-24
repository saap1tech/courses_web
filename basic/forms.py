from django import forms
from . import models

class AddVideo(forms.ModelForm):
    class Meta:
        model = models.Videos
        fields = ['video']

    def __init__(self, *args, **kwargs):
             super(AddVideo, self).__init__(*args, **kwargs)
             self.fields['video'].widget.attrs.update({
                 'id': 'video'
         })
