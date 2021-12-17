from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic 
from django.utils import timezone

from .models import Choice, Questions


# Create your views here.
class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_q_list'
    
    def get_queryset(self):
        return Questions.objects.filter(p_date__lte=timezone.now()).order_by('p_date')[:10]


class DetailsView(generic.DetailView):
    model = Questions
    template_name = 'polls/details.html'


class ResultsView(generic.DetailView):
    model = Questions
    template_name = 'polls/results.html'

def vote(request, question_id):
    question = get_object_or_404(Questions, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        context = {
            'question': question,
            'error_message': "You didnt selected a choice"
        }
        return render(request, 'polls/details.html', context)
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question_id,)))







 