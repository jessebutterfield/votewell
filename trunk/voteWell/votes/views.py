from django.template import Context, loader, RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.db.models import Count
from votes.models import Legislator, Bill, Comment
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from datetime import datetime

def home(request):
    if(request.user.is_authenticated()):
        t = loader.get_template('votes/home.html')
        comments = request.user.comment_set.all().order_by('-created')[:5]
        c = Context({'user': request.user,
                     'comments': comments})
    else:
        t = loader.get_template('welcome.html')
        c = Context({})
    return HttpResponse(t.render(c))

def state(request,state_abbr):
    legs = Legislator.objects.filter(state=state_abbr)
    t = loader.get_template('votes/state.html')
    c = Context({
                 'legs': legs,
    })
    return HttpResponse(t.render(c))

    

def legislatorDetail(request,leg_id):
    leg = Legislator.objects.get(pk=leg_id)
    bills = leg.bill_set.all()
    t = loader.get_template('votes/legislator.html')
    c = Context({
                 'leg': leg,
                 'bills': bills,})
    return HttpResponse(t.render(c))

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
        
    c = {'bill': bill,
         'roll': roll,
         'voteMatrix': voteMatrix,
         'commentMatrix': commentMatrix,}
    return render_to_response('votes/bill.html', c,
                               context_instance=RequestContext(request))


def billComment(request,bill_id):
    b = get_object_or_404(Bill, pk=bill_id)
    sentiment = request.POST['comment']
    text = request.POST['commentText']
    c = Comment(bill=b,user=request.user,text=text,sentiment=sentiment,created=datetime.now())
    c.save()
    return HttpResponseRedirect(reverse('votes.views.billDetail', args=(b.id,)))

