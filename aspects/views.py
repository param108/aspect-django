from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import JsonResponse
from models import Aspect, Future, Moment, belt
def getAspectsObject():
  aspects = Aspect.objects.all()
  ret = []
  for aspect in aspects:
    obj = {}
    obj['name'] = aspect.name
    obj['id'] = aspect.id
    obj['score'] = aspect.score
    obj['belt'] = belt(aspect.belt)

    # now append futures
    future = Future.objects.filter(aspect_id=aspect.id).order_by('-id')
    obj['futures'] = []
    idx = 0
    for f in future:
      obj1 = {}
      obj1['future'] = f.future
      obj1['id'] = f.id
      obj1['status'] = f.status
      obj1['seq'] = f.seq
      obj['futures'].append(obj1)
      # send the last 5 futures
      if idx < 5:
        idx += 1
      else:
        break

    # now append moments
    obj['moments'] = []
    moments = Moment.objects.filter(aspect_id=aspect.id).filter(status__exact="in progress").order_by('plan')
    for m in moments:
      obj1 = {}
      obj1['moment'] = m.moment
      obj1['plan'] = m.plan
      obj['moments'].append(obj1)
    ret.append(obj)
  return ret

# Create your views here.
@ensure_csrf_cookie
def aspectsList(request):
  return JsonResponse(
    { 'status': 0, 
      'data': getAspectsObject()
    }
  )

def addAspect(request):
  if request.method == "POST":
    name = request.POST.get("name","")
    if len(name):
      aspect = Aspect(name=name)
      aspect.save();
  return JsonResponse(
    { 'status': 0, 
      'data': getAspectsObject()
    }
  )
