from django.shortcuts import get_object_or_404, render
from django.views import generic

from .models import AgencyDetail, AgentAWBList, Location, Bank, Payments

# Create your views here.


def index(request):
    """
    View function for home page of site.
    """
    # Generate counts of some of the main Objects
    num_agents=AgencyDetail.objects.all().count()
    num_locations=Location.objects.all().count()
    num_banks=Bank.objects.all().count()
    num_payments = Payments.objects.all().count()
    num_non_fully_utilized_payments=Payments.objects.filter(payment_utilized=False).count()

    return render(request, 'index.html', context={'num_agents': num_agents, 'num_locations': num_locations,'num_banks': num_banks, 'num_payments': num_payments, 'num_non_fully_utilized_payments': num_non_fully_utilized_payments})


# class AgencyListView(generic.ListView):
#      model = AgencyDetail
#
#
# class AgencyDetailView(generic.DetailView):
#     model = AgencyDetail


# def index(request):
#     agency_list = AgencyDetail.objects.order_by
#     context = {'agency_list': agency_list}('agency_name')
#     return render(request, 'NahcoTrack/index.html', context)


# def awblist(request, agency):
#     return render(request, 'NahcoTrack/awblist.html', {'agentawblist': agentawblist})

