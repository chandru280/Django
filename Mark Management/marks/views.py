from django.http import JsonResponse
from django.shortcuts import render
from django.db import IntegrityError 
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from marks.forms import MarkForm, Registrationform, StaffForm, StandardForm, StudentForm, SubjectFormSet, TestSelectionForm, TestnameForm, TestsubjectFormSet
from marks.models import Mark, Staff, Standard, Student, Subject, Testname, Testsubject, UserForm

# from .decorators import admin_required 
from .decorators import can_add_required, can_update_required, can_delete_required
from django.http import HttpResponseForbidden
from django.contrib.auth.hashers import make_password

from django.contrib import messages



def register(request):
    if request.method == 'POST':
        form = Registrationform(request.POST)
        if form.is_valid():
            try:
                user = form.save(commit=False)
                
                user.save()
           
                
                return redirect('login')
            except IntegrityError as e:
                    
                    error_message = "Error: " + str(e)
                    return render(request, 'signup.html', {'form': form, 'error_message': error_message})

    else:
        form = Registrationform()
    return render(request, 'signup.html', {'form': form})


 

def user_login(request):
    if request.user.is_authenticated:
        return render(request, 'login.html', {'already_logged_in': True})

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        next_url = request.POST.get('next', 'home')   
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful')
            
            if user.role == 'ADMIN':
                return redirect('home')   
            elif user.role == 'STAFF':
                return redirect('home')   
            elif user.role == 'STUDENT':
                student = get_object_or_404(Student, roll_number=user)
                return redirect('student_detail', student_id=student.id)
            else:
                return redirect(next_url)   
        else:
            messages.error(request, 'Invalid username or password')
            return render(request, 'login.html', {
                'error_message': 'Invalid username or password.',
                'next': next_url   
            })
    
    next_url = request.GET.get('next', '')  
    return render(request, 'login.html', {'next': next_url})
@login_required
def user_logout(request):
    logout(request)
    return redirect('login')



@login_required
def manage_user_permissions(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("You do not have permission to access this page.")
    elif request.method == 'POST':
        for user in UserForm.objects.all():
            user.can_add = f'user_{user.id}_can_add' in request.POST
            user.can_update = f'user_{user.id}_can_update' in request.POST
            user.can_delete = f'user_{user.id}_can_delete' in request.POST
            user.save()

        return redirect('manage_user_permissions')
    
    users = UserForm.objects.all()
    return render(request, 'manage_user_permissions.html', {'users': users})


# @admin_required
# @can_add_required
def add_or_update_standard(request, standard_id=None):
    if standard_id:
        standard = get_object_or_404(Standard, id=standard_id)
    else:
        standard = None  

    if request.method == 'POST':
        standard_form = StandardForm(request.POST, instance=standard)
        formset = SubjectFormSet(request.POST, instance=standard)
        if standard_form.is_valid() and formset.is_valid():
            standard = standard_form.save()
            subjects = formset.save(commit=False)
            for subject in subjects:
                subject.standard = standard
                subject.save()
            formset.save_m2m()   
            return redirect('standard_list')   
    else:
        standard_form = StandardForm(instance=standard)
        formset = SubjectFormSet(instance=standard)

    return render(request, 'add_standart_with_subject.html', {
        'standard_form': standard_form,
        'formset': formset,
        'standard_id': standard_id,
    })

def delete_standard(request, standard_id):
    standard = get_object_or_404(Standard, id=standard_id)
    if request.method == 'POST':
        standard.delete() 
        return redirect('standard_list')  
    return redirect('standard_list')  




def standard_list(request):
    standards = Standard.objects.all()
    return render(request, 'standard_list.html', {'standards': standards})

def subject_list(request, standard_id):
    standard = Standard.objects.get(pk=standard_id)
    subjects = standard.subject_set.all()
    return render(request, 'subject_list.html', {'standard': standard, 'subjects': subjects})

def delete_subject(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    if request.method == 'POST':
        standard_id = subject.standard.id  
        subject.delete() 
        return redirect('subject_list', standard_id=standard_id)   
    return redirect('subject_list', standard_id=subject.standard.id)  


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
            return redirect('create_testname_with_subjects')
    else:
        testname_form = TestnameForm()
        formset = TestsubjectFormSet()

    return render(request, 'add_test.html', {
        'testname_form': testname_form,
        'formset': formset,
    })

def fetch_subjects(request):
    standard_id = request.GET.get('standard_id')
    subjects = Subject.objects.filter(standard_id=standard_id).values('id', 'name')
    print(standard_id)
    print(subjects)
    print('---------------------------------------------------------')
    return JsonResponse(list(subjects), safe=False)




def add_student(request): 
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid(): 
            student = form.save()
            
            user = UserForm(
                username=student.roll_number,
                password=make_password(student.date_of_birth.strftime('%Y-%m-%d')),   
                role='STUDENT',
                email=student.email,
                name=student.name,
            )
            user.save()
            
            return redirect('student_list')
    else:
        form = StudentForm()
    return render(request, 'add_student.html', {'form': form})


def student_list(request):
    students = Student.objects.all()
    return render(request, 'student_list.html', {'students': students})

def student_detail(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    marks = Mark.objects.filter(student=student)
    last_test = Testname.objects.last()  
    
    return render(request, 'student_detail.html', {
        'student': student,
        'marks': marks,
        'last_test': last_test,
    })

def update_student(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('student_detail', student_id=student_id)
    else:
        form = StudentForm(instance=student)
    return render(request, 'update_student.html', {'form': form, 'student': student})

def delete_student(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    if request.method == 'POST':
        student.delete()
        return redirect('student_list')
    return render(request, 'delete_student.html', {'student': student})







def staff_list(request):
    staff = Staff.objects.all()
    return render(request, 'staff_list.html', {'staff': staff})

def staff_add(request):
    if request.method == 'POST':
        form = StaffForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('staff_list')
    else:
        form = StaffForm()
    return render(request, 'staff_add.html', {'form': form})

def staff_update(request, staff_id):
    staff = get_object_or_404(Staff, pk=staff_id)
    if request.method == 'POST':
        form = StaffForm(request.POST, request.FILES, instance=staff)
        if form.is_valid():
            form.save()
            return redirect('staff_list')
    else:
        form = StaffForm(instance=staff)
    return render(request, 'staff_update.html', {'form': form})


def staff_delete(request, staff_id):
    staff = get_object_or_404(Staff, pk=staff_id)
    if request.method == 'POST':
        staff.delete()
        return redirect('staff_list')
    return render(request, 'staff_delete.html', {'staff': staff})

 




def create_marks(request, student_id):
    mark_forms = []
    student = get_object_or_404(Student, id=student_id)
    last_test = Testname.objects.last()

    if request.method == 'POST':
        test_form = TestSelectionForm(request.POST)
        if test_form.is_valid():
            student = test_form.cleaned_data['student']
            test = test_form.cleaned_data['test']
            subjects = Testsubject.objects.filter(test_name=test)

            for subject in subjects:
                total_mark = subject.total_mark
                pass_mark = subject.pass_mark
                mark_form = MarkForm(request.POST, prefix=str(subject.id), subject=subject)
                mark_form.initial['total_mark'] = total_mark
                mark_form.initial['pass_mark'] = pass_mark
                mark_forms.append(mark_form)

            if all(mf.is_valid() for mf in mark_forms):
                for mf in mark_forms:
                    mark = mf.save(commit=False)
                    mark.student = student
                    mark.test = test
                    mark.subject = Testsubject.objects.get(id=int(mf.prefix))  # Ensure correct subject reference
                    mark.status = mf.initial.get('status')  # Get the status from the initial data
                    mark.save()
                return redirect('success_url')
            else:
                print("Mark forms errors:", [mf.errors for mf in mark_forms])
        else:
            print("Test form errors:", test_form.errors)
    else:
        test_form = TestSelectionForm(initial={'student': student, 'test': last_test}, student=student)
        subjects = Testsubject.objects.filter(test_name=last_test)
        mark_forms = [MarkForm(prefix=str(subject.id), subject=subject) for subject in subjects]
        # test_form = TestSelectionForm(student=student) 
    return render(request, 'mark_form.html', {
        'test_form': test_form,
        'mark_forms': mark_forms,
    })




def get_subjects(request):
    test_id = request.GET.get('test')
    subjects = Testsubject.objects.filter(test_name_id=test_id)
    data = {'subjects': list(subjects.values('id', 'subject'))}
    return JsonResponse(data)



def update_mark(request, mark_id):
    mark = get_object_or_404(Mark, pk=mark_id)
    student = mark.student
    test = mark.test

    # Get the corresponding Testsubject instance
    test_subject = mark.subject

    if request.method == 'POST':
        form = MarkForm(request.POST, instance=mark)
        if form.is_valid():
            form.save()
            return redirect('student_detail', student_id=student.id)
        else:
            print(form.errors)  # Print any validation errors
    else:
        # Pass the total_mark and pass_mark from the Testsubject instance
        form = MarkForm(instance=mark, subject=test_subject, initial={
            'total_mark': test_subject.total_mark,
            'pass_mark': test_subject.pass_mark
        })

    return render(request, 'mark_update.html', {
        'form': form,
        'student': student,
        'test': test,
    })























