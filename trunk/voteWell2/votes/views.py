from django.template import Context, loader, RequestContext
from django.contrib.auth.models import User 
from django.contrib.auth import authenticate, login
from django.shortcuts import render_to_response, get_object_or_404
from django.db.models import Count
from votes.models import Legislator, Bill, Comment, Subject
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from datetime import datetime

def register(request):
    if(request.user.is_authenticated()):
        return HttpResponseRedirect(reverse('votes.views.home'))
    c = {'request':request}
    return render_to_response('votes/register.html',c,context_instance=RequestContext(request))
    
def submitRegistration(request):
    try:
        User.objects.get(user=request.POST['newusername'])
        print "Sorry that username is taken"
        return
    except:
        if(request.POST['mpassword']==request.POST['confirm']):
            User.objects.create_user(request.POST['newusername'],request.POST['email'],
                                    request.POST['mpassword'])
            
            user = authenticate(username=request.POST['newusername'], 
                                password=request.POST['mpassword'])
            login(request,user)
            return HttpResponseRedirect(reverse('votes.views.home'))
def home(request):
    if(request.user.is_authenticated()):
        comments = request.user.comment_set.all().order_by('-created')[:5]
        c = Context({'request': request,
                     'comments': comments})
        return render_to_response('votes/home.html',c,context_instance=RequestContext(request))

    else:
        c = Context({'request':request})
        return render_to_response('votes/welcome.html',c,context_instance=RequestContext(request))

def state(request,state_abbr):
    legs = Legislator.objects.filter(state=state_abbr)
    c = Context({ 'request':request,
                 'legs': legs,
    })
    return render_to_response('votes/state.html',c,context_instance=RequestContext(request))


    

def legislatorDetail(request,leg_id):
    leg = Legislator.objects.get(pk=leg_id)
    bills = leg.bill_set.all()
    c = Context({'request':request,
                 'leg': leg,
                 'bills': bills,})
    return render_to_response('votes/legislator.html',c,context_instance=RequestContext(request))


def billDetail(request,bill_id):
    bill = Bill.objects.get(pk=bill_id)
    votes = []
    if(bill.roll_set.count()>0):
        roll = bill.roll_set.all()[0]
        votes = roll.vote_set.all()
    else:
        roll = []
    comments = bill.comment_set.annotate(Count("sentiment")).order_by("sentiment","-created")
    numAye = 0
    numNay = 0
    if(len(comments)>0):
        if(comments[0].sentiment == '+'):
            numAye = comments[0].sentiment__count
        if(comments[numAye].sentiment == '-'):
            numNay = comments[numAye].sentiment__count
    commentMatrix = [comments[0:min(numAye,5)],comments[numAye:numAye+min(numNay,5)],
                     comments[numAye+numNay:numAye+numNay+5]]    
    voteMatrix = [[],[],[],[]]
    voteOptions = ['+','-','P','0']
    for vote in votes:
        voteMatrix[voteOptions.index(vote.vote)].append(vote)   
        
    c = {'request': request,
         'bill': bill,
         'roll': roll,
         'voteMatrix': voteMatrix,
         'commentMatrix': commentMatrix,}
    return render_to_response('votes/bill.html', c,context_instance=RequestContext(request))


def billComment(request,bill_id):
    if(request.user.is_authenticated()):
        b = get_object_or_404(Bill, pk=bill_id)
        sentiment = request.POST['comment']
        text = request.POST['commentText']
        com = Comment(bill=b,user=request.user,text=text,sentiment=sentiment,created=datetime.now())
        com.save()
        return HttpResponseRedirect(reverse('votes.views.billDetail', args=(b.id,)))
    else:
        return HttpResponseRedirect(reverse('votes.views.register'))
    
def search(request):
        
    c = {'request': request,}
    return render_to_response('votes/search.html',c,context_instance=RequestContext(request))

def searchSubmit(request,search_type):
    #TODO figure out switch statements in Python
    results = {}
    if(search_type == 'bills'):
        query = request.POST['query'].split()
        results['bills'] = Bill.objects.all()
        results['subjects'] = Subject.objects.all()
        for q in query:
            results['bills'] = results['bills'].filter(title__title__icontains=q).distinct()
            results['subjects'] = results['subjects'].filter(name__icontains=q)
        c = {'request': request,
             'results': results,}
        return render_to_response('votes/results.html',c,context_instance=RequestContext(request))
        
        