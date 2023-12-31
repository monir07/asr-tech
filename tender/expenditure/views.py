import datetime
from django.db import transaction
from django.db.models import Q, Prefetch, Sum, Value
from django.shortcuts import get_object_or_404, render, HttpResponseRedirect
from django.views import generic
from django.urls import reverse_lazy
from django.http.response import HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.template import loader
from django.http import HttpResponse
from ..models import DailyExpendiature
from .forms import ProjectExpendiatureForm

class ExpendatureDashboardView(generic.TemplateView):
    title = 'Dashboard'
    template_name="tender/expendature/dashboard.html"
    url_list = {
                'url_1':['tender_project_create', 'Daily Expendature', 'fa fa-caret-square-o-right'],
                'url_2':['tender_project_create', 'Security Money', 'fa fa-comments-o'],
                'url_3':['tender_project_create', 'PG Entry', 'fa fa-sort-amount-desc'],
                'url_4':['tender_project_create', 'Loan Entry', 'fa fa-check-square-o'],
            }

    def get_context_data(self, **kwargs):
        kwargs['url_list'] = self.url_list
        kwargs['title'] = self.title
        return super().get_context_data(**kwargs)
    

class ExpenditureCreateView(generic.CreateView):
    model = DailyExpendiature
    form_class = ProjectExpendiatureForm
    template_name = 'tender/tender_project/form.html'
    success_message = "Created Successfully."
    title = 'New Expenditure Form'
    success_url = "tender_project_list"
    
    def form_valid(self, form, *args, **kwargs):
        form.instance.created_by = self.request.user
        messages.success(self.request, self.success_message)
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return HttpResponseRedirect(reverse_lazy(self.success_url))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        return context


class ExpenditureUpdateView(generic.UpdateView):
    model = DailyExpendiature
    form_class = ProjectExpendiatureForm
    template_name = 'tender/tender_project/form.html'
    success_message = "Created Successfully."
    title = 'Expenditure Update Form'
    # success_url = "tender_project_list"
    
    def form_valid(self, form, *args, **kwargs):
        form.instance.updated_by = self.request.user
        messages.success(self.request, self.success_message)
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return HttpResponseRedirect(reverse_lazy(self.success_url))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        return context


class ExpenditureListView(generic.ListView):
    title = 'Tender Project List'
    model = DailyExpendiature
    context_object_name = 'items'
    paginate_by = 10
    template_name = 'tender/tender_project/list.html'
    queryset = DailyExpendiature.objects.filter()
    search_fields = ['project_name', 'job_no']
    list_display = ['total_amount', 'paid_method', 'expendiature_type']
    url_list = ['tender_project_update', 'tender_project_delete', 'tender_project_details']

    def get_queryset(self):
        queryset = super().get_queryset()
        query_param = self.request.GET.copy()
        search_param = query_param.get('query', None)
        queryset = queryset.filter(tour_id = self.kwargs.get('pk'))
        if search_param:
            Qr = format_search_string(self.search_fields, search_param)
            queryset = queryset.filter(Qr)
        return queryset
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['basic_template'] = basic_list.get(str(self.request.user.username), "common_user/common_user_home.html")
        context['fields'] = get_fields(self.model, self.list_display)
        context['delete_url'] = self.extra_urls[1]
        context['navigation_urls'] = self.navigation_urls
        context['extra_urls'] = self.extra_urls
        return context


class ExpenditureDetailView(generic.DetailView):
    model = DailyExpendiature
    context_object_name = 'instance'
    pk_url_kwarg = 'pk'
    # template_name = 'pdf-template/sample.html'
    template_name = 'tender/tender_project/details.html'
    title = "Expenditure Details"


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['basic_template'] = ''
        context['title'] = self.title
        return context


class ExpenditureDeleteView(generic.edit.DeleteView):
    model = DailyExpendiature
    success_url = 'tender_project_list'
    template_name = 'components/delete_confirm.html'
    success_message = 'Deleted Successfully!'

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            return HttpResponseRedirect(reverse_lazy(self.success_url))
        else:
            self.object = self.get_object()
            self.object.delete()
            messages.success(self.request, self.success_message)
            return HttpResponseRedirect(reverse_lazy(self.success_url))