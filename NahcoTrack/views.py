from django.shortcuts import get_object_or_404, render

from .models import AgencyDetail, AgentAWBList

# Create your views here.


def index(request):
    agency_list = AgencyDetail.objects.order_by('agency_name')
    context = {'agency_list': agency_list}
    return render(request, 'NahcoTrack/index.html', context)


def awblist(request, agency):
    return render(request, 'NahcoTrack/awblist.html', {'agentawblist': agentawblist})


# def eventaction(request):
#     if request.method == 'POST':
#
#         form=EventActionForm(request.POST)
#
#         if form.is_valid():
#             event_code = request.POST.get('event_code','')
#             event_actions = request.POST.get('event_actions','')
#             event_obj = EventActions(event_code=event_code,event_actions=event_actions)
#             event_obj.save()
#
#             return render(request, 'NahcoTrack/eventaction.html', {'event_obj': event_obj, 'is_registered':True})
#         else:
#             form = EventActionForm()
#
#             return render(request, 'NahcoTrack/eventaction.html', {'form': form})
#
#
# def eventactions(request):
#     all_events = EventActions.objects.all()
#     return render(request, 'NahcoTrack/eventactions.html',{'all_events': all_events})