from django.template import Context, loader
from votes.models import Legislator
from django.http import HttpResponse

def state(request,state_abbr):
    legs = Legislator.objects.filter(state=state_abbr)
    t = loader.get_template('votes/state.html')
    c = Context({
        'legs': legs,
    })
    return HttpResponse(t.render(c))
