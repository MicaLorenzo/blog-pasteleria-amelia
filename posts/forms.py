from django import forms

from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["titulo", "contenido", "imagen"]
        widgets = {
            "titulo": forms.TextInput(attrs={"placeholder": "Título del post"}),
            "contenido": forms.Textarea(attrs={"rows": 8}),
        }

    def clean_titulo(self):
        titulo = self.cleaned_data["titulo"].strip()
        if len(titulo) < 5:
            raise forms.ValidationError("El título debe tener al menos 5 caracteres.")
        return titulo
