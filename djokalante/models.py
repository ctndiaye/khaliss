from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator, MaxLengthValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.
class StatutObjet(models.TextChoices):
    INSERT = ("insert", _("INSERT"))
    UPDATE = ("update", _("UPDATE"))
    DELETE = ("delete", _("DELETE"))


class BaseModel(models.Model):
    class Meta:
        abstract = True
        managed = False

    date_creation = models.DateTimeField(name='date_creation', auto_now_add=True)
    date_modification = models.DateTimeField(name='date_modification', auto_now=True)
    statut = models.CharField(name='statut', max_length=6, choices=StatutObjet.choices, null=False, blank=False)


class Action(models.Model):
    class Meta:
        abstract = False
        ordering = ['name']

    action_code = models.CharField(max_length=12, blank=False, help_text="Code de l'action")
    name = models.CharField(max_length=50, blank=False, help_text="Nom de l'action")
    nivel = models.IntegerField(null=False, validators=[MinValueValidator(1), MaxValueValidator(5)],
                                help_text="Niveau de l'action'")
    action_parent = models.ForeignKey('Action', on_delete=models.DO_NOTHING, help_text="Parent de l'action")


class Banque(BaseModel):

    class Meta:
        abstract = False
        ordering = ['name']

    name = models.CharField(max_length=50, blank=False, help_text="Nom de la banque")
    account_number = models.CharField(max_length=50, blank=False, help_text="Numero de compte de la banque")
    address = models.TextField(max_length="255", blank=False, help_text="Adresse de la banque")
    phone = models.CharField(max_length=20, blank=False, help_text="Telefone de la banque")
    bank_rate = models.DecimalField(decimal_places=2, max_digits=4, help_text="Taux de la banque")

    user_creator = models.ForeignKey('Utilisateur', null=False, on_delete=models.DO_NOTHING,
                                     related_name='user_banque_create')
    user_modificator = models.ForeignKey('Utilisateur', null=False, on_delete=models.DO_NOTHING,
                                         related_name='user_banque_modify')


class Carte(BaseModel):
    class Meta:
        abstract = True
        ordering = ['product']

    product = models.CharField(max_length=50, blank=False, help_text="m du produit carte")
    expiration_date = models.DateField(null=False, help_text="Date d'expiration de la carte")
    card_state = models.CharField(max_length=10, blank=True, help_text="Statut de la carte")

    user_creator = models.ForeignKey('Utilisateur', null=False, on_delete=models.DO_NOTHING,
                                     related_name='user_carte_create')
    user_modificator = models.ForeignKey('Utilisateur', null=False, on_delete=models.DO_NOTHING,
                                         related_name='user_carte_modify')


class Commercant(BaseModel):
    class Meta:
        abstract = False
        ordering = ["social_reson"]

    social_reson = models.CharField(max_length=50, blank=False, help_text="Raison sociale du commercant")
    phone = models.CharField(max_length=50, blank=False, help_text="Telephone du commercant")
    address = models.TextField(max_length="255", blank=False, help_text="Adresse du commercant")
    status = models.CharField(max_length=10, blank=True, help_text="STatus du commercant")
    mercahnd_code = models.CharField(max_length=10, blank=False, help_text="Code du marchand")

    user_creator = models.ForeignKey('Utilisateur', null=False, on_delete=models.DO_NOTHING,
                                     related_name='user_commercant_create')
    user_modificator = models.ForeignKey('Utilisateur', null=False, on_delete=models.DO_NOTHING,
                                         related_name='user_commercant_modify')


class Compte(BaseModel):
    class Meta:
        abstract = False
        ordering = ['last_name', 'first_name', 'email']

    phone = models.CharField(max_length=20, blank=False, help_text="Telephone du compte")
    last_name = models.CharField(max_length=20, blank=False, help_text="Nom lie au compte")
    first_name = models.CharField(max_length=50, blank=False, help_text="Nom lie au compte")
    address = models.TextField(max_length=255, blank=False, help_text="Adresse du compte")
    email = models.EmailField(max_length=50, blank=False, help_text="Email du compte")
    piece_type = models.ForeignKey("TypePiece", null=False, related_name="compte_type_piece",
                                   on_delete=models.DO_NOTHING)
    piece_number = models.CharField(max_length=50, blank=False, help_text="Numero de la piece")
    card_number = models.CharField(max_length=50, blank=False, help_text="Numero de la carte")
    expiration_date = models.DateTimeField(null=False, help_text="Date d'expiration")
    secret_code = models.CharField(max_length=255, blank=False, help_text="Code secret")
    solde = models.DecimalField(decimal_places=2, max_digits=10, help_text="Solde du compte")
    account_status = models.CharField(max_length=10, blank=False, help_text="Statut du compte")
    card_status = models.CharField(max_length=10, blank=False, help_text="Statut de la carte")

    user_creator = models.ForeignKey('Utilisateur', null=False, on_delete=models.DO_NOTHING,
                                     related_name='user_compte_create')
    user_modificator = models.ForeignKey('Utilisateur', null=False, on_delete=models.DO_NOTHING,
                                         related_name='user_compte_modify')


class Devise(BaseModel):
    class Meta:
        abstract = False
        ordering = ['name']

    name = models.CharField(max_length=50, blank=False)
    code = models.CharField(max_length=3, blank=False)

    user_creator = models.ForeignKey('Utilisateur', null=False, on_delete=models.DO_NOTHING,
                                     related_name='user_devise_create')
    user_modificator = models.ForeignKey('Utilisateur', null=False, on_delete=models.DO_NOTHING,
                                         related_name='user_devise_modify')


class Employeur(BaseModel):
    class Meta:
        abstract = False
        ordering = ["social_reson", "account_number"]

    social_reson = models.CharField(max_length=50, blank=False, help_text="Raison sociale de l'entreprise")
    account_number = models.CharField(max_length=50, blank=False, help_text="Numero de compte de l'employeur")
    address = models.TextField(blank=False, help_text="Adresse de l'employeur")
    phone = models.CharField(max_length=20, blank=False, help_text="Telephone de l'employeur")
    account = models.DecimalField(max_digits=10, decimal_places=2, null=False, help_text="Solde de l'employeur")

    user_creator = models.ForeignKey('Utilisateur', null=False, on_delete=models.DO_NOTHING,
                                     related_name='user_employeur_create')
    user_modificator = models.ForeignKey('Utilisateur', null=False, on_delete=models.DO_NOTHING,
                                         related_name='user_employeur_modify')


class Journalisation(models.Model):
    event = models.CharField(max_length=200, blank=False,
                             help_text="Colonne d'information sur la ligne de journalisation")
    description = models.TextField(max_length=1000, blank=False, help_text='Description de la journalisation')
    date_event = models.DateTimeField(auto_now_add=True)


class Guichet(BaseModel):
    class Meta:
        abstract = False
        ordering = ['name', 'phone']

    pays_guichet = models.ForeignKey('Pays', null=False, on_delete=models.DO_NOTHING, help_text='Pays du guichet')
    name = models.CharField(max_length=100, blank=False, help_text='Nom du guichet')
    adress = models.TextField(max_length=1000, blank=False, help_text='Addresse du guichet')
    phone = models.CharField(max_length=20, blank=False, help_text='Telephone du guichet')
    account = models.DecimalField(max_digits=20, decimal_places=2, null=False, help_text='Solde du guichet')
    account_number = models.CharField(max_length=50, validators=[MaxLengthValidator(50)], null=False,
                                      help_text='Numero de compte du guichet')

    user_creator = models.ForeignKey('Utilisateur', null=False, on_delete=models.DO_NOTHING,
                                     related_name='user_guichet_create')
    user_modificator = models.ForeignKey('Utilisateur', null=False, on_delete=models.DO_NOTHING,
                                         related_name='user_guichet_modify')


class HistoriqueFichierVirement(BaseModel):
    class Meta:
        abstract = False

    file_name = models.CharField(max_length=100, blank=False, help_text="Nom du fichier")
    account = models.CharField(max_length=30, blank=False, help_text="Numero de compte")
    employe = models.ForeignKey('Employeur', null=False, help_text="Numero de l'employeur",
                                related_name="hfv_employeur", on_delete=models.DO_NOTHING)

    user_creator = models.ForeignKey('Utilisateur', null=False, on_delete=models.DO_NOTHING,
                                     related_name='user_hfv_create')
    user_modificator = models.ForeignKey('Utilisateur', null=False, on_delete=models.DO_NOTHING,
                                         related_name='user_hfv_modify')


class Motif(BaseModel):
    class Meta:
        abstract = False
        ordering = ['libelle']

    libelle = models.CharField(max_length=100, blank=False, help_text='Nom du motif')

    user_creator = models.ForeignKey('Utilisateur', null=False, on_delete=models.DO_NOTHING,
                                     related_name='user_motif_create')
    user_modificator = models.ForeignKey('Utilisateur', null=False, on_delete=models.DO_NOTHING,
                                         related_name='user_motif_modify')


class ParametreApplication(BaseModel):
    class Meta:
        abstract = False

    name = models.CharField(max_length=50, blank=False, help_text="Nom de l'operateur")
    address = models.TextField(blank=False, help_text="Adresse de l'operateur")
    zip_code = models.CharField(max_length=10, null=True, help_text="Code postal")
    phone = models.CharField(max_length=20, blank=False, help_text="Telephone de l'operateur")
    fax = models.CharField(max_length=20, blank=False, help_text="Fax de l'oerateur")
    version_number = models.CharField(max_length=50, blank=False, help_text="Numero de version deploye")
    licence = models.CharField(max_length=50, blank=False, help_text="Numero de licence")
    seuil_solde = models.DecimalField(decimal_places=2, max_digits=10, null=False, help_text="Seuil d'envoi journalier")
    opeartor_part = models.DecimalField(decimal_places=2, max_digits=10, null=False, help_text="Part de l'operateur")
    expeditor_part = models.DecimalField(decimal_places=2, max_digits=10, null=False, help_text="Part de l'expediteur")
    payer_part = models.DecimalField(decimal_places=2, max_digits=10, null=False, help_text="Part du payeur")
    plafond_journalier = models.DecimalField(decimal_places=2, max_digits=10, null=False,
                                             help_text="Plafond d'envoi journalier")
    duree_validite_code = models.DecimalField(decimal_places=2, max_digits=30, null=False,
                                              help_text="Duree de validite du code")


class Pays(BaseModel):
    class Meta:
        abstract = False
        ordering = ['name']

    name = models.CharField(max_length=50, null=False, unique=True, help_text="Le nom du pays")
    code = models.CharField(max_length=3, null=False, help_text="Le code du pays")
    devise_pays = models.ForeignKey('Devise', null=False, on_delete=models.DO_NOTHING, related_name="devise")

    user_creator = models.ForeignKey('Utilisateur', null=False, on_delete=models.DO_NOTHING,
                                     related_name='user_pays_create')
    user_modificator = models.ForeignKey('Utilisateur', null=False, on_delete=models.DO_NOTHING,
                                         related_name='user_pays_modify')


class Profil(BaseModel):
    class Meta:
        abstract = False
        ordering = ['name']

    name = models.CharField(max_length=30, blank=False, help_text="Profil de l'utilisateur")
    actions = models.ManyToManyField('Action', blank=False, help_text="")

    user_creator = models.ForeignKey('Utilisateur', null=False, on_delete=models.DO_NOTHING,
                                     related_name='user_profil_create')
    user_modificator = models.ForeignKey('Utilisateur', null=False, on_delete=models.DO_NOTHING,
                                         related_name='user_profil_modify')


class Programme(BaseModel):
    class Meta:
        abstract = False
        ordering = ['name', 'description', 'promotor_name']

    name = models.CharField(max_length=50, blank=False, help_text="Nom du programme")
    description = models.TextField(blank=False, help_text="Description du programme")
    start_date = models.DateTimeField(blank=False, help_text="Date de debut du programme")
    end_date = models.DateTimeField(blank=False, help_text="Date de fin du programme")
    promotor_name = models.CharField(max_length=30, blank=False, help_text="Nom du promoteur")
    promotor_phone = models.CharField(max_length=20, blank=False, help_text="Telephone du promoteur")
    promotor_addres = models.TextField(blank=False, help_text="Telephone du promoteur")
    account = models.DecimalField(max_digits=10, decimal_places=2, help_text="Solde de la promotion")
    subscrib_number = models.DecimalField(max_digits=10, decimal_places=2, help_text="Nombre d'inscription")

    user_creator = models.ForeignKey('Utilisateur', null=False, on_delete=models.DO_NOTHING,
                                     related_name='user_programme_piece_create')
    user_modificator = models.ForeignKey('Utilisateur', null=False, on_delete=models.DO_NOTHING,
                                         related_name='user_programme_modify')


class Promotion(BaseModel):
    class Meta:
        abstract = False
        ordering = ['libelle', 'description']

    libelle = models.CharField(max_length=100, blank=False, help_text='Nom de la promotion')
    description = models.TextField(blank=False, help_text='Description de la promotion')
    date_debut = models.DateField(blank=False, help_text='Date de debut de la promotion')
    date_fin = models.DateField(blank=False, help_text='Date de fin de la promotion')
    porcentage = models.DecimalField(blank=False, help_text='Pourcentage de la romotion', decimal_places=2,
                                     max_digits=5)

    user_creator = models.ForeignKey('Utilisateur', null=False, on_delete=models.DO_NOTHING,
                                     related_name='user_promotion_create')
    user_modificator = models.ForeignKey('Utilisateur', null=False, on_delete=models.DO_NOTHING,
                                         related_name='user_promotion_modify')


class Transfert(BaseModel):
    class Meta:
        abstract = False
        ordering = ['expeditor_last_name', 'expeditor_first_name', 'beneficiaire_last_name', 'beneficiaire_first_name']

    operation_code = models.CharField(max_length=100, blank=False, help_text="Code de l'operation")
    operation_number = models.CharField(max_length=100, blank=False, help_text="Numero de l'operation")
    expeditor_first_name = models.CharField(max_length=50, blank=False, help_text="Nom de l'expediteur")
    expeditor_last_name = models.CharField(max_length=50, blank=False, help_text="prenom de l'expediteur")
    expeditor_phone = models.CharField(max_length=20, blank=False, help_text="telephone de l'expediteur")
    expeditor_piece = models.CharField(max_length=20, blank=False, help_text="Piece de l'expediteur")
    send_date = models.DateField(auto_now_add=True, blank=False, help_text="Date d'envoie")
    account = models.DecimalField(max_digits=7, decimal_places=2, blank=False, help_text="Date d'envoie")
    commission_account = models.DecimalField(max_digits=7, decimal_places=2, blank=False, help_text="Date d'envoie")
    beneficiaire_first_name = models.CharField(max_length=50, blank=False, help_text="Nom du bénéficiaire")
    beneficiaire_last_name = models.CharField(max_length=50, blank=False, help_text="prenom du beneficiaire")
    beneficiaire_piece = models.CharField(max_length=50, blank=False, help_text="Piece du beneficiaire")
    beneficiaire_phone = models.CharField(max_length=20, blank=False, help_text="telephone de l'expediteur")
    state = models.CharField(max_length=50, blank=False, help_text="Etat de la transaction")
    reception_date = models.DateField(auto_now_add=True, blank=False, help_text="Date de reception")
    cancel_date = models.DateField(auto_now_add=True, blank=False, help_text="Date d'annulation")

    motif = models.ForeignKey('Motif', null=False, on_delete=models.DO_NOTHING,
                              related_name='motif_transfert')
    propotion = models.ForeignKey('Promotion', null=False, on_delete=models.DO_NOTHING,
                                  related_name='promotion_transfert')

    user_creator = models.ForeignKey('Utilisateur', null=False, on_delete=models.DO_NOTHING,
                                     related_name='user_transfert_create')
    user_modificator = models.ForeignKey('Utilisateur', null=False, on_delete=models.DO_NOTHING,
                                         related_name='user_transfert_modify')


class TypePiece(BaseModel):
    class Meta:
        abstract = False
        ordering = ['name']

    name = models.CharField(max_length=30, blank=False, help_text="Type de la piece")

    user_creator = models.ForeignKey('Utilisateur', null=False, on_delete=models.DO_NOTHING,
                                     related_name='type_piece_create')
    user_modificator = models.ForeignKey('Utilisateur', null=False, on_delete=models.DO_NOTHING,
                                         related_name='type_piece_modify')


class Utilisateur(AbstractUser):
    class Meta:
        abstract = False
        ordering = ['last_name', 'first_name']

    adresse = models.TextField(name='adresse', null=False, help_text="Adresse de l'utilisateur")
    telephone = models.CharField(name='telephone', max_length=20, unique=True, null=False,
                                 help_text="Telephone de l'educatrice")
    date_creation = models.DateTimeField(name='date_creation', auto_now_add=True)
    date_modification = models.DateTimeField(name='date_modification', auto_now_add=True)
    statut = models.CharField(name='statut', max_length=6, choices=StatutObjet.choices, null=False, blank=False)

    user_pays = models.ForeignKey('Pays', null=True, help_text="Pays de l'utilisateur", on_delete=models.DO_NOTHING)

    user_creator = models.ForeignKey('Utilisateur', null=True, on_delete=models.DO_NOTHING,
                                     related_name='user_create')
    user_modificator = models.ForeignKey('Utilisateur', null=True, on_delete=models.DO_NOTHING,
                                         related_name='user_modify')

    USERNAME_FIELD = "username"

    REQUIRED_FIELDS = ["last_name", "first_name", "adresse", "telephone", 'email']

    FIELDS_DIC = {'id', 'adresse', 'telephone', 'date_creation', 'date_modification', 'statut', 'email'}

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return f'User("{self.first_name}", "{self.last_name}")'
