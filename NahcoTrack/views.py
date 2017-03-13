from django.shortcuts import get_object_or_404, render

from .models import AgencyDetail, AgentAWBList
# Create your views here.


def index(request):
    agency_list = AgencyDetail.objects.order_by('agency_name')
    context = {'agency_list': agency_list}
    return render(request, 'NahcoTrack/index.html', context)


def awblist(request, agency):
    return render(request, 'NahcoTrack/awblist.html', {'agentawblist': agentawblist})