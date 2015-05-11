# -*- coding: utf-8 -*-

import json
import django_tables2 as tables

from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.core.context_processors import csrf
from django.contrib.auth import logout


from django.template import RequestContext

from django.utils import timezone

from MonEtablissement.models import MesActivite, MesClasse, \
                                    MesSequence, MesNiveaux, User, Eleve, \
                                    MesQuestion, MesReponse, Domaine, ProgressionEleve
from forms import LoginForm, MessageForm, StudentProfileForm, UserForm, QuestionsForm
from django.forms.widgets import Select



# Create your views here.

#===============================================================================
# Creation de la vue Index sur les Niveaux
#===============================================================================
#  2. Codage raccourci avec méthode render()
def index(request, logged_user=None, *args):
    """
    Main Index Page: Expose only current year MesClasse.niveau
    """
    
    current_year_classes_list = MesClasse.objects.filter(annee_cours_dateint=timezone.datetime.today().year).order_by("niveau")
    niveau_list = MesNiveaux.objects.filter()
    context = {'current_year_classes_list': current_year_classes_list, 'niveau_list': niveau_list}
    
    try:
        email = request.POST['email']
        context.update({'email':email})
    except:
        pass
    
    if logged_user:
        context.update({'logged_user': logged_user})
    
    #render(objet requête, garabit, contexte rempli <dict> (variable))
    return render(request, 'MonEtablissement/index_bs.html', context)


    

def sequence(request, niveau_int):
    """
    View all (current year) sequences for a unique level
    """

    #recupère la liste de sequence associée au niveau (Backward lookup from Foreign key)
    b=MesNiveaux.objects.get(niveau=niveau_int)
#     b.messequence_set.all()
    
#     sequence_list = MesSequence.objects.filter(niveau=b)
    
    sequence_list = MesSequence.objects.filter(niveau=b).select_related("domaine").order_by('ordre')
     
    domaine = []
    for d in sequence_list:
        if d.domaine:
            domaine.append((d,d.domaine))
        else:
            domaine.append((d,"#cdcdcd"))
        
    context = {'sequence_list': sequence_list, 'niveau_int':niveau_int, 'domaine':domaine}
    
    #USAGE: render(objet requête, garabit, contexte rempli <dict> (variable) **kwargs)
    return render(request, 'MonEtablissement/sequence_bs.html', context)



# def iteractivities(seq_id):
#     """
#     Coroutine
#     generator pour iterer sur un set de question/reponse
#     http://stackoverflow.com/questions/231767/what-does-the-yield-keyword-do-in-python
#     """
#     
#     #retrieve all sequences:
#     seance_list = MesSeance.objects.filter(ma_sequence = seq_id) 
#     
#     activities = MesActivite.objects.filter(ma_sequence = seance_list)
#     
#     for act in activities:
#         #Retrieve associated activities to the current sequence
#         activities = MesActivite.objects.filter(ma_sequence = seq_id)
#         for activity in activities:
#             questions = MesQuestion.objects.filter(activite = activity)
#             #retrieve questions for a given activit
#         yield seance, activities
        

def seance(request,niveau_int, seq_id):
    """
    View all seances for a given sequence
    
    A seance is bound to a sequence. Several seance can point to the same sequence to 
    keep an history of activity that have been build.
    
    A Seance references one or more associated activities that are:
        - Interactive question Forms
        - Video
        - Documents
    
    """
#     #retrieve all sequences:
#     seance_list = MesSeance.objects.filter(ma_sequence = seq_id) 
#     #select current seance
# #     current_seance = TODO
#     
#     #Retrieve associated activities to the current sequence
#     activities = Mes Activités.objetcs.filter(ma_seance = seance)
#     for s in seance:
#         output ="you are looking seance "+unicode(s)  +" from sequence "+unicode(seq_id)
#     return HttpResponse(output)

#     content = iteractivities(seq_id)
    activities = MesActivite.objects.filter(ma_sequence = seq_id)
    
    l = []
    
    #Consomme generator
    for activity in activities:
#         activities = c[1]  
#         for activity in act:
            questions = MesQuestion.objects.filter(activite = activity)
            l.append([activity,questions])
    
    #rebuild generator
    content = activities
    
    
    return render (request, 'MonEtablissement/activities_bs.html', {'content': content, 'activities':l})
    
    
    
    pass

def login(request):
    """
    Méthode qui instancie un formulaire de login 
    OU
    Vérifie que les id. de connexion ont été entrés correctement avant redirection vers /welcome
    """
    form = LoginForm()
    if (request.method == 'POST'):
        #recup. le POST et le passe dans un objet formulaire pour 
        #faire usage de form.is_valid
        #OU
        #construit empty form pour redemander les id. connexion
        form = LoginForm(request.POST or None)
        if form.is_valid():
            #Recupère le nom d'utilisateur renseigné par l'utilisateur dans le LoginForm
            user_name = form.cleaned_data['username'] 
            #Recupere l'entrée correspondante dans le modèle User
            logged_user = User.objects.get(username=user_name) 
            #Passe l'identificateur à l'objet request 
            request.session['logged_user_id'] = logged_user.id 
            return HttpResponseRedirect('/welcome')
    return render(request,'MonEtablissement/login.html', {'form': form})


def logout_view(request):
    """
    Methode to logout and redirect to welcome page
    """
    logout(request)
    # Redirect to entry page.
    return HttpResponseRedirect('/welcome')


def get_logged_user_from_request(request):
    """
    Protection des pages privées 
    
    TODO: distinguer les connexions eleves/professeur pour proposer une 
          page d'administration professeur
    """
    
    if 'logged_user_id' in request.session: 
        logged_user_id = request.session['logged_user_id']
        logged_user = User.objects.get(id=logged_user_id)
        return logged_user
    else:
        return None
    
    
def show_profile(request):
    """
    Creation d'une vue pour afficher le profil utilisateur
    
    TODO: Finaliser la distinction eleve/professeur de la méthode:
            get_logged_user_from_request
    TODO: 
            
    """
    logged_user = get_logged_user_from_request(request)
    if logged_user.is_superuser:
        #Hello teacher!
        
        #Récuperer la liste des classes pour l'année en cours
        
        #Si date comprise entre septembre et 31 décembre alors année_en_cours = timezone.datetime.today().year
        #Si date comprise entre 01 janvier et 31 aout alors année_en_cours = ( timezone.datetime.today().year - 1 )
        
        if timezone.datetime.today().month > 9:
            classe_en_cours = MesClasse.objects.filter(annee_cours_dateint = timezone.datetime.today().year)
        else:           
            classe_en_cours = MesClasse.objects.filter(annee_cours_dateint = timezone.datetime.today().year - 1 )
        
        
        
        return render_to_response ('MonEtablissement/show_profile.html',
                                   {'user_to_show': logged_user,  'classe_en_cours': classe_en_cours , 'mois': timezone.datetime.today().month } )
    # Le paramètre n'a pas été trouvé
    else:
        return HttpResponseRedirect('/login')

def welcome(request):
    """
    Renvoi vers page d'acceuil avec identification
    """
    logged_user = get_logged_user_from_request(request)
    
    if logged_user:
        return index(request, logged_user=logged_user)
    
    #kept for reference - replaced by the generic get_logged_user_from_request()
#     if 'logged_user_id' in request.session:
#         logged_user_id = request.session['logged_user_id']
#         logged_user = User.objects.get(id=logged_user_id)
#         return index(request, logged_user=logged_user)

    else:
        return HttpResponseRedirect('/login')
    
def process_questionform(request):
    """
    Process submitted answer from a question form
    """
    
    
    pass    


def exampleform(request):
    """
    test crispy forms
    """
    # This view is missing all form handling logic for simplicity of the example
    return render(request, 'MonEtablissement/exampleform.html', {'form': MessageForm()}) 


def register(request):
    """
    User registration
    """
       
    if len(request.POST) > 0:
        
        
        # Create form instances from POST data or build empty ones
        if 'password' in request.POST:
            user_form = UserForm(request.POST)
            student_form = StudentProfileForm()
        if 'ma_classe' in request.POST:
            student_form = StudentProfileForm(request.POST)
            user_form = UserForm()
            
        if user_form.is_valid():
            
            # Save a new User object from the form's data.
            user_form.save()
            # Retrieve the username from the last POST
            username = request.POST.get('username')
            #Retrieve the underlying User object from DB
            user = User.objects.get(username=username)
            #User is anctive by default
            user.is_active = False
            user.save()
            
            #Create an non-validating object
            eleve = student_form.save(commit=False)
            #Pass it the desired user foreign key
            eleve.user = user
            #build a new "partial + Non validated" StudentProfileForm using the eleve instance
            student_form = StudentProfileForm(None, instance=eleve)
            return render(request,'MonEtablissement/user_profile.html', {'student_form': student_form})
            
        elif student_form.is_valid():
            
            student_form.save(commit=True)
            return HttpResponseRedirect('/login')
        
        elif not user_form.has_changed() and not user_form.is_valid() and user_form.is_bound :
            #user_form: Case not valid, including empty form
            return render (request, 'MonEtablissement/user_profile.html', {'user_form': user_form}) 
        
        elif not student_form.is_valid() and student_form.is_bound :
            
            return render (request, 'MonEtablissement/user_profile.html', {'student_form': student_form})
            
        else:
            return render (request, 'MonEtablissement/user_profile.html', {'user_form': user_form})
    else:
        user_form = UserForm()
        student_form = StudentProfileForm()
        
        return render (request, 'MonEtablissement/user_profile.html', {'user_form': user_form, 'student_form': student_form})

def iterquestions(activity_id = None):
    """
    Coroutine
    generator pour iterer sur un set de question/reponse
    http://stackoverflow.com/questions/231767/what-does-the-yield-keyword-do-in-python
    """
    #get random questions - dev 
    if not activity_id:
        questions = MesQuestion.objects.order_by('?')
        
        for question in questions:
            reponse = MesReponse.objects.select_related().filter(question = question)
            yield question, reponse
    
    #get specific questions bound to an activity
    else:
        questions = MesQuestion.objects.filter(activite = activity_id)
        for question in questions:
            reponse = MesReponse.objects.select_related().filter(question = question)
            yield question, reponse


class Results_Table(tables.Table):
    """
    Create a simple table from ProgressionEleve
    https://pypi.python.org/pypi/django-tables2
    
    todo: Sort by activity!
    
    """
    
    nom = tables.Column(accessor = 'eleve.user.first_name' )
    prenom = tables.Column(accessor = 'eleve.user.last_name' )
    id_eleve = tables.Column(accessor='eleve.id')
    #active = tables.Column(accessor = 'eleve.user.is_active' )
    
    class Meta:
        model = ProgressionEleve
        # add class="paleblue" to <table> tag
        attrs = {"class": "paleblue"}
        fields = ('activite', 'resultat', 'attempt','question', 'date', 'id_eleve')
        sequence = ('prenom', 'nom')
        
class Final_Result_Table(tables.Table):
    """
    A custom table to compile all results from eleve for a given sequence
    """
    nom = tables.Column()
    prenom = tables.Column()
    note = tables.Column()
    class Meta:
        # add class="paleblue" to <table> tag
        attrs = {"class": "paleblue"}
    
  
        
def Results_simple_list(request,classe_id = None, seq_id = None):
    """
    Serve results for admin/teacher
    """
    
    #get activity id for seq_id:
    mes_activite_list = MesActivite.objects.all().filter(ma_sequence = seq_id  )   
    
    #build the queryset from all model objects
    eleve_list = Eleve.objects.all().filter(ma_classe = classe_id)    
    queryset = ProgressionEleve.objects.all().filter(activite__in=mes_activite_list, eleve__in=eleve_list ).select_related('eleve')
                                                                                              
    table = Results_Table(queryset)
    
    # Build a table that give final result for a given sequence
    global_dict = {}
    global_result = []
    note = None
    
    for entry in queryset:
        #Build a dict. to pass to django-tables:
        try:
            note = global_dict[entry.eleve]
            note_new = entry.resultat + note
            global_dict.update({entry.eleve: note_new})   
        except KeyError:
            global_dict.update({entry.eleve: entry.resultat})
        
        
    for i in global_dict.items():
        
#         user = Eleve.objects.all().get(id = i[0].id)
        user = Eleve.objects.all().filter(id = i[0].id).select_related('user')
        global_result.append({'nom': user[0].user.last_name, 'prenom':user[0].user.first_name, 'note': i[1]})
#         global_result.append({i[0]:i[1]})
    
    table_final = Final_Result_Table(global_result)
        
    
    
    # style the table
    tables.RequestConfig(request).configure(table)
    tables.RequestConfig(request).configure(table_final)
    
    context = {"table": table, "table_final":table_final, "sequence": MesSequence.objects.all().get(id=seq_id), "classe":MesClasse.objects.all().get(id=classe_id)}
    
    
    #USAGE: render(objet requête, garabit, contexte rempli <dict> (variable) **kwargs)
    return render(request, 'MonEtablissement/result_table.html', context)
    

def my_results(request, classe_id = None, niveau_int = None):
    """
    Classe pour:
    
        - donner accès à l'ensemble des résultats par séquence
        pour un classe donnée
        - Réutilise template "élève" pour selection de séquence
    """
    
    #recupère la liste de sequence associée au niveau (Backward lookup from Foreign key)
    b = MesNiveaux.objects.get(niveau=niveau_int)
    sequence_list = MesSequence.objects.filter(niveau=b).select_related("domaine").order_by('ordre')
     
    domaine = []
    for d in sequence_list:
        if d.domaine:
            domaine.append((d,d.domaine))
        else:
            domaine.append((d,"#cdcdcd"))
        
    context = {'sequence_list': sequence_list, 'niveau_int':niveau_int, 'domaine':domaine, 'classe_id':classe_id }
    
    #USAGE: render(objet requête, garabit, contexte rempli <dict> (variable) **kwargs)
    return render(request, 'MonEtablissement/results_bs.html', context)
#     output ="you are looking sequences at "+unicode(etablissement_text)+" niveau "+niveau_int+" eme" 
#     return HttpResponse(output)
    
    
    return HttpResponse(classe_niveau)
    pass

def my_questionform(request,activity_id = None ):
    """
    Classe pour:
    
        - instancier un formulaire de question/reponse
        - Process submitted answer from a question form
        
    TODO: select proper question/reponse
    """
    #prepare a form; QCM
    form = QuestionsForm()
    #Fetch question/reponse to specific activity
    if not activity_id:
        for question, reponse in iterquestions():
            form.add_question(question, reponse)
    elif activity_id:
        for question, reponse in iterquestions(activity_id):
            form.add_question(question, reponse)
            
    form.close()
    output = "bonjour "
    reptext = ""
    note = 0
    
    if len(request.POST) > 0:
        
        #process POST answer and write results to UserDB
        for question, reponse in iterquestions():
            if request.POST.get(question.enonce):
                #logic to process Q/A
                count = 0
                for rep in reponse:
                    if rep.verify:
                        break
                
                if int(request.POST.get(question.enonce)) == count:
                    #reponse juste
                    reptext+="<p>Question "+unicode(question.enonce)+" reponse juste </p>"
                    note += question.valeur
                else:
                    #reponse fausse
                    reptext+="<p>Question "+unicode(question.enonce)+" reponse fausse </p>"
                
#                 reptext +=str(count)+" "+request.POST.get(question.enonce)                  
#                 output +="Question "+unicode(question.enonce)+" position "+unicode(request.POST.get(question.enonce))+ " reponse "+reptext
                
            else:
                #answer is wrong or nothing has been submitted
                pass
        
        #TODO:
        # At this point a new entry is written if student decide to submit a new answer to
        # a question he already answer. DateTimeField allow to select the most up-to-date answer
        # A better way would be to update the previous entry using the auto_now True option!
        
        #create  and save an object that:
        #1. identify the user
        #2. identify the activity he completed + retrieve "niveau" from attached sequence
        #3. Check if a corresponding entry exists SELECT...WHERE...
        #4. save his score (UPDATE or INSERT depending on 3.)
        # Kept for reference: retrieve activity bjet without related "Sequence" from foreign key 
        # activity = MesActivite.objects.filter(id = activity_id)[0]
        # DB "one hitter" get objets and related object follow foreign keys
        activity = MesActivite.objects.select_related('ma_sequence').get(id = activity_id )
        sequence_id = activity.ma_sequence.id
        niveau = activity.ma_sequence.niveau
        
        # USER AUTHENTIFICATION    
        logged_user = get_logged_user_from_request(request)
        
        if not logged_user:
            #Form won't be process
            return render(request, 'MonEtablissement/completed_bs.html', {'activity_id': activity_id, 'redo': True, 'niveau': niveau,
                                                                          'sequence_id':sequence_id, 'anonymous_user': True})
        
        if logged_user and not logged_user.is_active:
            #user nno-actif
            return HttpResponse("Non actif")
        
        if logged_user:
            output += logged_user.username
        output += reptext
        

        #get() queryset; Only one result shoud be expected
        try:
            progeleve = ProgressionEleve.objects.all().get(activite=activity, eleve = Eleve.objects.all().get(user = logged_user))
        except ProgressionEleve.DoesNotExist:
            ProgressionEleve.objects.create(eleve = Eleve.objects.all().get(user = logged_user), resultat = note, activite=activity )
            return render(request, 'MonEtablissement/completed_bs.html', {'activity': activity_id, 'niveau': niveau, 'sequence_id': sequence_id})
            
#             return HttpResponse(output)
        
        except ProgressionEleve.MultipleObjectsReturned:
            pass
        
        #Else; UPDATE object (note/question/attempt)
        progeleve.resultat = note
        progeleve.attempt = progeleve.attempt + 1
        progeleve.question = request.POST.get('question_eleve')
        progeleve.save()
        
        return render(request, 'MonEtablissement/completed_bs.html', {'activity_id': activity_id, 'redo': True, 'niveau': niveau, 'sequence_id':sequence_id})
            
    
            
    else:

        return render(request, 'MonEtablissement/questionform.html', {'form': form, 'test': activity_id})
        

def pdf_view(request):
    """
    Classe pour servir un document PDF au sein du navigateur
    Requiert l'installation du plugin de lecture PDF côté client
    """
    
    #format url - remove leading '/' form request.path
      
    with open(request.path[1:], 'r') as pdf:
        response = HttpResponse(pdf.read(),content_type='application/pdf')
        response['Content-Disposition'] = 'filename=some_file.pdf'
        return response
    pdf.closed
    
    
def png_view(request):
    """
    Classe pour servir un document 'image/png' au sein du navigateur
    """
    
    #format url - remove leading '/' form request.path
      
    with open(request.path[1:], 'r') as png:
        response = HttpResponse(png.read(),content_type='image/png')
        response['Content-Disposition'] = 'filename=some_file.png'
        return response
    png.closed
    
    
def mp4_view(request):
    """
    Classe pour servir un document 'image/png' au sein du navigateur
    """
    
    #format url - remove leading '/' form request.path
      
    with open(request.path[1:], 'r') as mp4:
        response = HttpResponse(mp4.read(),content_type='video/mp4')
        response['Content-Disposition'] = 'filename=some_file.mp4'
        return response
    mp4.closed


def your_view(request):
    poll_results = [4, 6, 7, 1]
    poll_as_json = json.dumps(poll_results)
    # Gives you a string '[4, 6, 7, 1]'
    return render(request, 'MonEtablissement/testd3js.html', {'poll_as_json': poll_as_json}) 
    