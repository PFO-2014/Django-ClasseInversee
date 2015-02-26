# -*- coding: utf-8 -*-

import json


from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.core.context_processors import csrf

from django.template import RequestContext

from django.utils import timezone

from MonEtablissement.models import MesActivite, MesClasse, MesSeance,\
                                    MesSequence, MesNiveaux, User, Eleve, \
                                    MesQuestion, MesReponse, Domaine, ProgressionEleve
from forms import LoginForm, MessageForm, StudentProfileForm, UserForm, QuestionsForm



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


# def iter_sequence(sequence_list):
#     """
#     """
#     
#     for sequence in sequence_list:
#         if sequence.domaine_f:
#             yield sequence, sequence.domaine_f
#         else:
#             yield sequence, "ploup"
    

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
#     output ="you are looking sequences at "+unicode(etablissement_text)+" niveau "+niveau_int+" eme" 
#     return HttpResponse(output)


def iteractivities(seq_id):
    """
    Coroutine
    generator pour iterer sur un set de question/reponse
    http://stackoverflow.com/questions/231767/what-does-the-yield-keyword-do-in-python
    """
    
    #retrieve all sequences:
    seance_list = MesSeance.objects.filter(ma_sequence = seq_id) 
    
    for seance in seance_list:
        #Retrieve associated activities to the current sequence
        activities = MesActivite.objects.filter(ma_seance = seance)
#         for activity in activities:
#             questions = MesQuestion.objects.filter(activite = activity)
#             #retrieve questions for a given activit
        yield seance, activities
        
        

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

    content = iteractivities(seq_id)
    
    l = []
    
    #Consomme generator
    for c in content:
        activities = c[1]  
        for activity in activities:
            questions = MesQuestion.objects.filter(activite = activity)
            l.append([activity,questions])
    
    #rebuild generator
    content = iteractivities(seq_id)
    
    
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
    """
    logged_user = get_logged_user_from_request(request)
    if logged_user:
        return render_to_response ('MonEtablissement/show_profile.html',
                                   {'user_to_show': logged_user})
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
            #Create an non-validating object
            eleve = student_form.save(commit=False)
            #Pass it the desired user foreign key
            eleve.user = user
            #build a new "partial + Non validated" StudentProfileForm using the eleve instance
            student_form = StudentProfileForm(None, instance=eleve)
            return render(request,'MonEtablissement/user_profile.html', {'student_form': student_form, 'username': str(student_form.helper.attrs)})
        
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


def my_questionform(request,activity_id = None ):
    """
    Classe pour:
    
        - instancier un formulaire de question/reponse
        - Process submitted answer from a question form
        
    TODO: select proper question/reponse
    """
    #prepare a form; QCM
    
    form = QuestionsForm()
    
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
                    note += 1
                else:
                    #reponse fausse
                    reptext+="<p>Question "+unicode(question.enonce)+" reponse fausse </p>"
                
#                 reptext +=str(count)+" "+request.POST.get(question.enonce)                  
#                 output +="Question "+unicode(question.enonce)+" position "+unicode(request.POST.get(question.enonce))+ " reponse "+reptext
                
            else:
                #answer is wrong or nothing has been submitted
                pass
            
        logged_user = get_logged_user_from_request(request)
        if logged_user:
            output += logged_user.username
        output += reptext
        
        #create and save an object that:
        #1. identify the user
        #2. identify the activity he completed
        #3. save his score
        activity = MesActivite.objects.filter(id = activity_id)[0]
        ProgressionEleve.objects.create(eleve = logged_user, resultat = note, activite=activity )
        # kept for reference: activity not referenced
        #ProgressionEleve.objects.create(eleve = logged_user, resultat = note)
        
        return HttpResponse(output)
        
        if len(request.POST.get('question_eleve'))==0:
            #formulaire vide
            return render(request, 'MonEtablissement/questionform.html', {'form': form})
            
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


def your_view(request):
    poll_results = [4, 6, 7, 1]
    poll_as_json = json.dumps(poll_results)
    # Gives you a string '[4, 6, 7, 1]'
    return render(request, 'MonEtablissement/testd3js.html', {'poll_as_json': poll_as_json}) 
    