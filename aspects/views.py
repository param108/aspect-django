from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import JsonResponse
from models import Aspect, Future, Moment, belt, SimpleValue
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

def getAspectsObject(user):
  aspects = Aspect.objects.filter(user=user)
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
@login_required
@ensure_csrf_cookie
def aspectsList(request):
  tid = request.POST.get("tid", -1)
  name = request.POST.get("name", "")
  return JsonResponse(
    { 'status': 0, 
      'data': getAspectsObject(request.user),
      'tid': tid,
      'name': name,
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

@csrf_exempt
def simpleValueRead(request):
  key = request.POST.get("key", -1)
  tid = request.POST.get("tid", -1)
  name = request.POST.get("name", "")
  ret = None
  if key == -1:
    ret = SimpleValue.objects.all().order_by('id');
    if len(ret) == 0:
      s = SimpleValue();
      s.save()
      return JsonResponse({'val': "",
                           'tid': tid,
                           'key': s.id,
                           'name': name});
    return JsonResponse({'val': ret[0].val,
                         'tid': tid,
                         'key': ret[0].id,
                         'name': name});
  else:
    ret = SimpleValue.objects.get(id=key)
    return JsonResponse({'val': ret.val,
                         'tid': tid,
                         'key': ret.id,
                         'name': name})

@csrf_exempt
def simpleValueWrite(request):
  key = request.POST.get("key", -1)
  name = request.POST.get("name", "")
  tid = request.POST.get("tid", -1)
  val = request.POST.get("val", "")
  ret = SimpleValue.objects.get(id=key)
  ret.val = val
  ret.save();
  return JsonResponse({'val': ret.val,
                         'tid': tid,
                       'key': ret.id,
                       'name': name})
