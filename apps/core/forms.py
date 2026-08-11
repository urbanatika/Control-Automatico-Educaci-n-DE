from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(label="Nombre", max_length=120)
    email = forms.EmailField(label="Correo electrónico")
    subject = forms.CharField(label="Asunto", max_length=150)
    message = forms.CharField(label="Mensaje", widget=forms.Textarea(attrs={"rows": 6}))
    honeypot = forms.CharField(required=False, widget=forms.HiddenInput)

    def clean_honeypot(self):
        value = self.cleaned_data.get("honeypot")
        if value:
            raise forms.ValidationError("No se pudo enviar el mensaje.")
        return value
