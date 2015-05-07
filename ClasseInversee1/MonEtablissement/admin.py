# -*- coding: utf-8 -*-

from django.contrib import admin
from MonEtablissement.models import MesClasse, MesSequence, \
    MesActivite, Eleve, MesNiveaux, MesQuestion, MesReponse, Domaine, \
    Competence, ProgressionEleve
from django.contrib.admin.helpers import Fieldset




class MesSequencesInline(admin.TabularInline):
    model = MesSequence
    extra = 1

class MesReponsesInline(admin.TabularInline):
    model = MesReponse
    extra = 1
    
class MesActiviteInline(admin.TabularInline):
    model = MesActivite
    extra = 1

class MesCompetenceInline(admin.TabularInline):
    model = Competence
    extra = 1



class MesClassesAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Mon établissement', {'fields': ['nom_etablissement_text']}),
        ('Niveau', {'fields': ['niveau']}),
        ('Année Scolaire', {'fields': ['annee_cours_dateint']}),
    ]
    inlines = [MesSequencesInline]

# class MesSeanceAdmin(admin.ModelAdmin):
#     inlines = [MesActiviteInline]
    
class MesSequenceAdmin(admin.ModelAdmin):
    list_display = ('short_description_sequence', 'niveau')
    list_filter = ('short_description_sequence', 'niveau')
    
    Fieldset = [
                ('Séquence', {'fields': ['short_description_sequence']}),
                ('Niveau', {'fields': ['niveau']})
                
    
                ]
    
    inlines = [MesCompetenceInline, MesActiviteInline]
    
class MesQuestionAdmin(admin.ModelAdmin):
    inlines = [MesReponsesInline]
    


# Register your models here.
admin.site.register(MesClasse, MesClassesAdmin)
admin.site.register(MesSequence, MesSequenceAdmin)
# admin.site.register(MesSeance, MesSeanceAdmin)
admin.site.register(MesActivite)
admin.site.register(Eleve)
admin.site.register(MesNiveaux)
admin.site.register(MesQuestion, MesQuestionAdmin)
admin.site.register(MesReponse)
admin.site.register(Domaine)
admin.site.register(ProgressionEleve)



