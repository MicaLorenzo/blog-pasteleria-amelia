from django import forms

from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["titulo", "contenido", "imagen"]
        labels = {
            "titulo": "Título",
            "contenido": "Contenido",
            "imagen": "Foto (opcional)",
        }
        widgets = {
            "titulo": forms.TextInput(attrs={"placeholder": "Ej: Chocotorta clásica"}),
            "contenido": forms.Textarea(
                attrs={"rows": 8, "placeholder": "Ingredientes, pasos, novedades..."}
            ),
        }

    def clean_titulo(self):
        titulo = self.cleaned_data["titulo"].strip()
        if len(titulo) < 5:
            raise forms.ValidationError("El título debe tener al menos 5 caracteres.")
        return titulo