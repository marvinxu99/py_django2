from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic


from .models import Question, Choice

# Create your views here.


def index(request):
    return render(request, 'polls/index.html')

# def question(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     template = loader.get_template('polls/index.html')
#     context = {
#         'latest_question_list': latest_question_list,
#     }
#     return HttpResponse(template.render(context, request))


class QuestionView(generic.ListView):
    template_name = 'polls/question.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]


# class DetailView(generic.DetailView):
#     model = Question
#     template_name = 'polls/detail.html'
def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    choices = question.choice_set.all()
    # next_q = Question.objects.filter(pub_date__gt=question.pub_date).order_by('pub_date').first()
    try:
        prev_q = question.get_previous_by_pub_date()
        prev_id = prev_q.id
    except:
        prev_id = 0

    try:
        next_q = question.get_next_by_pub_date()
        next_id = next_q.id
    except:
        next_id = 0

    return render(
        request,
        'polls/detail.html',
        {
            'question': question,
            'choices': choices,
            'prev_id': prev_id,
            'next_id': next_id
        }
    )


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
