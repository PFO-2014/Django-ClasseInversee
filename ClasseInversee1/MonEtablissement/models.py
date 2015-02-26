# -*- coding: utf-8 -*-


from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

import random


"""
CREATION DE LA BASE DE DONNEE
AJOUT DES METHODES DEDIEES
"""

#===============================================================================
# NIVEAU - pour relation n-n classe-sequence
#===============================================================================
class MesNiveaux(models.Model):
    """
    Classe définissant la base de donnée des niveaux
    """
    
    niveau = models.IntegerField('Niveau', unique=True)
    

    def __unicode__(self):
        return str(self.niveau)



#===============================================================================
# CLASSE -NIVEAU - ETABLISSEMENT - ANNEE SCOLAIRE
#===============================================================================
class MesClasse(models.Model):
    """
    Classe définissant la base de donnée des classes
    """
    nom_etablissement_text = models.CharField('mon établissement', max_length=200)
    annee_cours_dateint = models.IntegerField('Année en cours', default=timezone.datetime.today().year, editable=True)
    
#     niveau = models.IntegerField('Niveau')
    niveau = models.ForeignKey(MesNiveaux)

    def annee_en_cours(self):
        return self.annee_cours_dateint == timezone.datetime.today().year
    annee_en_cours.admin_order_field = 'annee_cours_dateint'
    annee_en_cours.short_description = 'année en cours'

    def __unicode__(self):
        return self.nom_etablissement_text+" "+str(self.niveau)+", "+str(self.annee_cours_dateint)
#===============================================================================
# DOMAINE
#===============================================================================

class Domaine(models.Model):
    """
    Consolidate Domain of Activity
    """
     
    nom = models.CharField(max_length=50, unique=True)
    color = models.CharField(max_length=7, default="#cdcdcd", unique=True)

    def save(self):
        if self.color=="#cdcdcd":
            r = lambda: random.randint(0,255)
            self.color = '#%06x' % ((r()+255)/2,(r()+255)/2,(r()+255)/2)
        super(Domaine, self).save()
    
    def __unicode__(self):
        return self.nom
    

    
    
#===============================================================================
# ELEVE
#===============================================================================
class Eleve(models.Model):
    """
    Definition d'un modèle d'élève
.    
    see API docs:
        https://docs.djangoproject.com/en/1.7/ref/contrib/auth/
        https://docs.djangoproject.com/en/1.7/topics/auth/default/#user-objects
    
    username
        Required. 30 characters or fewer. Usernames may contain alphanumeric, _, @, +, . and - characters.
    first_name
        Optional. 30 characters or fewer.
    last_name
        Optional. 30 characters or fewer.
    email
        Optional. Email address.
    password
        Required. A hash of, and metadata about, the password.
         (Django doesn’t store the raw password.) Raw passwords can be arbitrarily 
         long and can contain any character. See the password documentation.1
    """
    
    user = models.ForeignKey(User, unique=True)
    
    ma_classe = models.ForeignKey(MesClasse, blank=True, null=True)
    date_de_naissance = models.DateField(blank=True, null=True)
    
    def __unicode__(self):
        return str(self.user)
    
    #nom = models.CharField(max_length=30)
    #prenom = models.CharField(max_length=30)
    #courriel = models.EmailField()
    # mot_de_passe = models.CharField(max_length=32)
    #link to MesClasses
    

#===============================================================================
# SEQUENCE
#===============================================================================
class MesSequence(models.Model):
    """
    Classe définissant le modèle du chapitrage
    progression;...
    """
    #Description et référencement d'une séquence
    short_description_sequence = models.CharField("Nom de la séquence", max_length=200)
    full_description_sequence = models.TextField("Description d'une séquence", blank=True, null=True)
#     domaine = models.CharField("domaine et/ou thème", max_length=200, blank=True, null=True)
    
    #Foreign Keys
    niveau = models.ForeignKey(MesNiveaux,blank=True, null=True)
    ma_classe = models.ForeignKey(MesClasse,blank=True, null=True)
    domaine = models.ForeignKey(Domaine, blank=True, null=True)
 
    
    #Champs pour suivi de progression
    ordre = models.IntegerField('ordre de la séquence', blank=True, null=True)
    sequence_en_cours = models.BooleanField(default=False)

    
    def __unicode__(self):
        try:
            return self.short_description_sequence+" niveau "+str(self.ma_classe.niveau)+"eme"
        except:
            return self.short_description_sequence
        

#===============================================================================
# COMPETENCES
#===============================================================================

class Competence(models.Model):
    """
    Consolidate competences
    """
    
    description = models.CharField("description", max_length=250)
    sequence_f = models.ForeignKey(MesSequence, blank=True, null=True)
    
    
    def __unicode__(self):
        return self.description        


#===============================================================================
# SEANCES
#===============================================================================
class MesSeance(models.Model):
    """
    Classe définissant le modèle des séances
    Une séance références des activités
    activités; videos; exercices; 
    """
    short_description_seance = models.CharField("Objet de la séance", max_length=200)
    full_description_seance = models.TextField("Description d'une séance ", default='Description requise')
    #ressource_de_la_seance
    # http://code.google.com/p/django-selectreverse/
    
    #link to MesClasses
    ma_sequence = models.ForeignKey(MesSequence)
   
    def __unicode__(self):
        return self.short_description_seance
    
    
#===============================================================================
# ACTIVITE - FORMULAIRES - QUESTIONS - VIDEOS - DOCUMENTS
#===============================================================================
class MesActivite(models.Model):
    """
    Classe définissant le modèle des activités
    activités; videos; exercices;pdf...
    """
    short_description_activite = models.CharField("Type D'activité", max_length=200)
    full_description_activite = models.TextField("Enoncé ", default='Description requise pour cette activité')
    docfile = models.FileField(upload_to='documents/%Y/%m/%d',blank=True)

    
    ma_seance = models.ForeignKey(MesSeance)
    
    def __unicode__(self):
        return self.short_description_activite

#===============================================================================
# PROGRESSION ELEVE - RESULATS; PARTICIPATION
#===============================================================================    
class ProgressionEleve(models.Model):
    """
    Classe pour enregistrer l'activité des éléves et leurs résultats
    """
    eleve = models.ForeignKey(User)
    activite = models.ForeignKey(MesActivite,blank=True, null=True)
    #pour une activité, le résultat (niveau implicite porté par champ activite)
    #Blank; null si pas de participation à l'activité
    resultat = models.IntegerField('Note', blank=True, null=True)
    #Need write date to keep the most up-to-date answer
    date = models.DateTimeField('date', blank=True, null=True, auto_now_add=True)

#===============================================================================
# QUESTION 
#=============================================================================== 
class MesQuestion(models.Model):
    """
    Classe supportant l'insertion de question; incluant:
    - Enoncé
    - Facultativement: un document
    """
    #Foreign keys
    activite = models.ForeignKey(MesActivite)
    
    #champ propre
    enonce = models.TextField()
    resume = models.CharField('description succinte', max_length=200)
    
    def __unicode__(self):
        return self.resume
    
#===============================================================================
# REPONSE 
#=============================================================================== 
class MesReponse(models.Model):
    """
    Classe supportant les réponses à une question.
    - Default: Réponse unique, champ verify = True
    - alternative : plusieurs réponses ie:QCM
    """
        
    #Foreign keys
    question = models.ForeignKey(MesQuestion)
    
    #champ propre
    verify = models.BooleanField('Cette réponse est-elle juste?',default=True)
    reponse_text = models.CharField('une réponse textuelle', max_length=200,
                                    blank=True, null=True)

       