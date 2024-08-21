from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Quiz, Question, QuizResult
from .forms import TakeQuizForm, QuiznameForm, QuestionForm


def create_quiz(request):
    if request.method == 'POST':
        form = QuiznameForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('quiz_list')  
    else:
        form = QuiznameForm()
    
    return render(request, 'add_quiz.html', {'form': form })



def update_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)

    if request.method == 'POST':
        form = QuiznameForm(request.POST, instance=quiz)
        
        if form.is_valid() :
            form.save()
            return redirect('quiz_list')
    
    else:
        form = QuiznameForm(instance=quiz)
    
    return render(request, 'update_quiz.html', { 'form': form })



def create_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('quiz_list')  
    else:
        form = QuestionForm()
    
    return render(request, 'add_question.html', {'form': form })



def update_question(request, question_id):
    question = get_object_or_404(Question, id=question_id)

    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        
        if form.is_valid() :
            form.save()
            return redirect('quiz_list')
    
    else:
        form = QuestionForm(instance=question)
    
    return render(request, 'add_question.html', { 'form': form })


def quiz_list(request):
    quizzes = Quiz.objects.all()
    return render(request, 'quiz_list.html', {'quizzes': quizzes})

def quiz_detail(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    return render(request, 'quiz_detail.html', {'quiz': quiz})


def take_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    questions = Question.objects.filter(quiz=quiz)
    print('quiz:', quiz)
    print('questions:', questions)
    
    if request.method == 'POST':
        form = TakeQuizForm(request.POST, questions=questions)
        if form.is_valid():
            score = 0
            for question in questions:
                answer = form.cleaned_data[f'question_{question.id}']
                print('answer:', answer)
                print('correct answer:', question.answer)
                if answer.strip().lower() == question.answer.strip().lower():
                    score += 1
                print('correct acore:', score)

            QuizResult.objects.create(user=request.user, quiz=quiz, score=score)
            return redirect('quiz_list')
    else:
        form = TakeQuizForm(questions=questions)

    return render(request, 'take_quiz.html', {'quiz': quiz, 'form': form})


def leaderboard(request):
    results = QuizResult.objects.all().order_by('-score', '-date_taken')[:10]
    return render(request, 'leaderboard.html', {'results': results})
