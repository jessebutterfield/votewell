from django.template import Context, loader
from votes.models import Legislator, Bill
from django.http import HttpResponse

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
