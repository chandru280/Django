from django.forms import inlineformset_factory
from django.shortcuts import render
from django.shortcuts import render, redirect
from .forms import TestnameForm, TestsubjectFormSet, TestSelectionForm, MarkForm, MarkForm2
from django.http import JsonResponse
from .models import Testname, Testsubject, Mark

def create_testname_with_subjects(request):
    if request.method == 'POST':
        testname_form = TestnameForm(request.POST)
        formset = TestsubjectFormSet(request.POST)
        if testname_form.is_valid() and formset.is_valid():
            testname = testname_form.save()
            testsubjects = formset.save(commit=False)
            for testsubject in testsubjects:
                testsubject.test_name = testname
                testsubject.save()
            return redirect('create_testname_with_subjects')  # Replace 'success_url' with your desired success URL
    else:
        testname_form = TestnameForm()
        formset = TestsubjectFormSet()
    
    return render(request, 'add_test.html', {
        'testname_form': testname_form,
        'formset': formset,
    })



def create_marks(request):
    mark_forms = []

    if request.method == 'POST':
        print("POST data:", request.POST)
        test_form = TestSelectionForm(request.POST)
        if test_form.is_valid():
            student = test_form.cleaned_data['student']
            test = test_form.cleaned_data['test']
            subjects = Testsubject.objects.filter(test_name=test)
            mark_forms = [MarkForm(request.POST, prefix=str(subject.id), subject_name=subject.subject) for subject in subjects]
            if all([mf.is_valid() for mf in mark_forms]):
                for mf in mark_forms:
                    mark = mf.save(commit=False)
                    mark.student = student
                    mark.test = test
                    mark.subject_id = int(mf.prefix)
                    mark.save()
                return redirect('success_url') 
            else:
                print("Mark forms errors:", [mf.errors for mf in mark_forms])
        else:
            print("Test form errors:", test_form.errors)
    else:
        test_form = TestSelectionForm()

    return render(request, 'mark_form.html', {
        'test_form': test_form,
        'mark_forms': mark_forms,
    })


def get_subjects(request):
    test_id = request.GET.get('test')
    subjects = Testsubject.objects.filter(test_name_id=test_id)
    data = {'subjects': list(subjects.values('id', 'subject'))}
    return JsonResponse(data)



def manage_marks(request, test_id):
    test = Testname.objects.get(id=test_id)
    subjects = Testsubject.objects.filter(test_name=test)
    print(subjects)
    MarkFormSet = inlineformset_factory(Testname, Mark, form=MarkForm2, extra=len(subjects), can_delete=False)

    if request.method == 'POST':
        formset = MarkFormSet(request.POST, instance=test)
        if formset.is_valid():
            formset.save()
            return redirect('some_success_url')  # replace with your success URL
    else:
        formset = MarkFormSet(instance=test, queryset=Mark.objects.none())

    return render(request, 'manage_marks.html', {'formset': formset, 'test': test, 'subjects': subjects})
