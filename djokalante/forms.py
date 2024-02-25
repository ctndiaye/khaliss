from django import forms

from djokalante.models import Banque, Carte


class BanqueForm(forms.Form):
    id = forms.HiddenInput()
    name = forms.CharField(max_length=30, required=True, label="Nom de la banque")
    phone = forms.CharField(max_length=20, required=True, label="Telephone de la banque")
    address = forms.Textarea(required=True, label="Adresse de la banque")
    account_number = forms.CharField(max_length=50, required=True, label="Numero de compte de la banque")


class CarteForm(forms.Form):
    product = forms.ChoiceField(max_length=30, required=True, label="Nom du produit carte")
    expiration_date = forms.DateField(label="Date d'expiration", required=True)
    card_state = forms.ChoiceField(label="Statut de la carte", required=True)


class CommercantForm(forms.ModelForm):
    social_reson = forms.CharField(max_length=50, required=True, label="Raison sociale du commercant")
    phone = forms.CharField(max_length=50, required=True, label="Telephone du commercant")
    address = forms.TextField(max_length="255", required=True, label="Adresse du commercant")
    status = forms.CharField(max_length=10, blank=True, label="Statut du commercant")
    mercahnd_code = forms.CharField(max_length=10, required=True, help_text="Code du marchand")


class CompteForm(forms.Form):
    phone = forms.CharField(max_length=20, required=True, label="Telephone du compte")
    last_name = forms.CharField(max_length=20, required=True, label="Nom lie au compte")
    first_name = forms.CharField(max_length=50, required=True, label="Nom lie au compte")
    address = forms.TextField(max_length=255, required=True, label="Adresse du compte")
    email = forms.EmailField(max_length=50, required=True, label="Email du compte")
    piece_type = forms.ChoiceField(required=True, label="Type de Piece")
    piece_number = forms.CharField(max_length=50, required=True, label="Numero de la piece")
    card_number = forms.CharField(max_length=50, required=True, label="Numero de la carte")
    expiration_date = forms.DateTimeField(required=True, label="Date d'expiration")
    secret_code = forms.CharField(max_length=255, blank=False, label="Code secret")
    solde = forms.DecimalField(decimal_places=2, max_digits=10, label="Solde du compte")
    account_status = forms.CharField(max_length=10, blank=False, help_text="Statut du compte")
    card_status = forms.CharField(max_length=10, blank=False, help_text="Statut de la carte")
