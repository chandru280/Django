from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Quiz, Question, QuizResult
from .forms import TakeQuizForm

def quiz_list(request):
    quizzes = Quiz.objects.all()
    return render(request, 'quiz_list.html', {'quizzes': quizzes})

def quiz_detail(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    return render(request, 'quiz_detail.html', {'quiz': quiz})

@login_required
def take_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    questions = Question.objects.filter(quiz=quiz)

    if request.method == 'POST':
        form = TakeQuizForm(request.POST, questions=questions)
        if form.is_valid():
            score = 0
            for question in questions:
                answer = form.cleaned_data[f'question_{question.id}']
                if answer.is_correct:
                    score += 1
            QuizResult.objects.create(user=request.user, quiz=quiz, score=score)
            return redirect('quiz_list')
    else:
        form = TakeQuizForm(questions=questions)

    return render(request, 'take_quiz.html', {'quiz': quiz, 'form': form})

def leaderboard(request):
    results = QuizResult.objects.all().order_by('-score', '-date_taken')[:10]
    return render(request, 'leaderboard.html', {'results': results})
