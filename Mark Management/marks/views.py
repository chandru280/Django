from django.http import JsonResponse
from django.shortcuts import render
from django.db import IntegrityError 
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from marks.forms import *
from marks.models import *

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
                messages.success(request, 'Registration completed successfully')
                return redirect('login')
            except IntegrityError as e:
                    
                    error_message = "Error: " + str(e)
                    return render(request, 'authendication/signup.html', {'form': form, 'error_message': error_message})

    else:
        form = Registrationform()
    return render(request, 'authendication/signup.html', {'form': form})


 

def user_login(request):
    if request.user.is_authenticated:
        return render(request, 'authendication/login.html', {'already_logged_in': True})

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
            return render(request, 'authendication/login.html', {
                'error_message': 'Invalid username or password.',
                'next': next_url   
            })
    
    next_url = request.GET.get('next', '')  
    return render(request, 'authendication/login.html', {'next': next_url})



@login_required
def user_logout(request):
    logout(request)
    messages.success(request, 'Logout successful')
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
        messages.success(request, 'Permission modified for the use successful')
        return redirect('manage_user_permissions')
    
    users = UserForm.objects.all()
    return render(request, 'authendication/manage_user_permissions.html', {'users': users})



def academicyear(request):
    if request.method == 'POST':
        form = AcademicYearForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Academic year created successful')
            return redirect('home')
    else:
        form = AcademicYearForm()
    return redirect('home')
 


def home(request):
    current_year = request.session.get('selected_academic_year')
    academic_years = AcademicYear.objects.all()

    if current_year is None:
        academic_year = AcademicYear.objects.last()   
        if academic_year:   
            request.session['selected_academic_year'] = academic_year.year
            current_year = academic_year.year   

    form = AcademicYearForm()

    if request.method == "POST":
        selected_year = request.POST.get('academic_year')
        print('selected_year   ',selected_year)
        request.session['selected_academic_year'] = selected_year
        return redirect('home')

    students = Student.objects.filter(academic_year__year=current_year)
    return render(request, 'home.html', {'form':form, 'students': students, 'academic_years': academic_years, 'current_year': current_year})


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
            if standard:
                messages.success(request, 'Standard updated successful')
            else:
                messages.success(request, 'Standard created successful')

            return redirect('standard_list')   
    else:
        standard_form = StandardForm(instance=standard)
        formset = SubjectFormSet(instance=standard)

    return render(request, 'subject_standard/add_standart_with_subject.html', {
        'standard_form': standard_form,
        'formset': formset,
        'standard_id': standard_id,
    })



def delete_standard(request, standard_id):
    standard = get_object_or_404(Standard, id=standard_id)
    if request.method == 'POST':
        standard.delete() 
        messages.success(request, 'Standard deleted successful')
        return redirect('standard_list')  
    return redirect('standard_list')  




def standard_list(request):
    standards = Standard.objects.all()
    return render(request, 'subject_standard/standard_list.html', {'standards': standards})



def subject_list(request, standard_id):
    standard = Standard.objects.get(pk=standard_id)
    subjects = standard.subjects.all()
    return render(request, 'subject_standard/subject_list.html', {'standard': standard, 'subjects': subjects})



def delete_subject(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    if request.method == 'POST':
        standard_id = subject.standard.id  
        subject.delete() 
        messages.success(request, 'Subject deleted successful')
        return redirect('subject_list', standard_id=standard_id)   
    return redirect('subject_list', standard_id=subject.standard.id)  



def create_testname_with_subjects(request):
    current_year = request.session.get('selected_academic_year')   
    if request.method == 'POST':
        testname_form = TestnameForm(request.POST)
        formset = TestsubjectFormSet(request.POST)
        if testname_form.is_valid() and formset.is_valid():
            testname = testname_form.save(commit=False)
            academic_year = AcademicYear.objects.get(year=current_year)
            testname.academic_year = academic_year
            testname.save()
            testsubjects = formset.save(commit=False)
            for testsubject in testsubjects:
                testsubject.test_name = testname
                testsubject.save()
            messages.success(request, 'Test created successful')
            return redirect('create_testname_with_subjects')
    else:
        testname_form = TestnameForm()
        formset = TestsubjectFormSet()

    return render(request, 'subject_standard/add_test.html', {
        'testname_form': testname_form,
        'formset': formset,
    })



def fetch_subjects(request):
    standard_id = request.GET.get('standard_id')
    subjects = Subject.objects.filter(standard_id=standard_id).values('id', 'name')
    return JsonResponse(list(subjects), safe=False)




def add_student(request): 
    current_year = request.session.get('selected_academic_year')   
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid(): 
            student = form.save(commit=False)
            academic_year = AcademicYear.objects.get(year=current_year)
            student.academic_year = academic_year
            student.save()
            
            user = UserForm(
                username=student.roll_number,
                password=make_password(student.date_of_birth.strftime('%Y-%m-%d')),   
                role='STUDENT',
                email=student.email,
                name=student.name,
            )
            user.save()
            messages.success(request, 'Student created successful')
            return redirect('student_list')
    else:
        form = StudentForm()
    return render(request, 'student/add_student.html', {'form': form})



def student_list(request, standard_id):
    current_year = request.session.get('selected_academic_year')
    students = Student.objects.filter(academic_year__year=current_year, standard_id=standard_id)
    standard_id = Standard.objects.get(id=standard_id)
    return render(request, 'student/student_list.html', {'students': students, 'standard_id':standard_id})



def generate_register_numbers(request, standard_id):
    current_year = request.session.get('selected_academic_year')
    if request.method == 'GET':
        start_register = request.GET.get('start_register')

        start_register = int(start_register)
        standard = get_object_or_404(Standard, id=standard_id)

        students = Student.objects.filter(academic_year__year=current_year, standard=standard).order_by('name')
        
        if not students.exists():
            messages.warning(request, "No students found in the selected standard.")
            return redirect('student_list', standard_id=standard_id)

        for idx, student in enumerate(students, start=start_register):
            student.register_no = f"{idx:04d}"   
            student.save()
        standard.status = True
        standard.save()
        messages.success(request, "Register numbers have been successfully generated.")
        return redirect('student_list', standard_id=standard_id)
    else:
        return redirect('student_list', standard_id=standard_id)



def student_detail(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    marks = Mark.objects.filter(student=student)
    last_test = Testname.objects.last()  
    
    return render(request, 'student/student_detail.html', {
        'student': student,
        'marks': marks,
        'last_test': last_test,
    })



def update_student(request, student_id, standard_id):
    student = get_object_or_404(Student, pk=student_id)
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student Updated successfully')
            return redirect('student_list', standard_id=standard_id)    
    else:
        form = StudentForm(instance=student)
    return render(request, 'student/update_student.html', {'form': form, 'student': student})




def delete_student(request, student_id, standard_id):
    student = get_object_or_404(Student, pk=student_id)
    if request.method == 'POST':
        student.delete()
        messages.success(request, 'Student deleted successfully')
        return redirect('student_list', standard_id=standard_id)  
    return redirect('student_list', standard_id=standard_id)



def staff_add(request):
    if request.method == 'POST':
        form = StaffForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Staff created successful')
            return redirect('staff_list')
    else:
        form = StaffForm()
    return render(request, 'staff/staff_add.html', {'form': form})



def staff_list(request):
    staff = Staff.objects.all()
    return render(request, 'staff/staff_list.html', {'staff': staff})



def staff_detail(request, staff_id):
    staff = get_object_or_404(Staff, pk=staff_id)
    
    return render(request, 'staff/staff_detail.html', {
        'staff': staff,
    
    })


def staff_update(request, staff_id):
    staff = get_object_or_404(Staff, pk=staff_id)
    if request.method == 'POST':
        form = StaffForm(request.POST, request.FILES, instance=staff)
        if form.is_valid():
            form.save()
            messages.success(request, 'Staff updated successful')
            return redirect('staff_list')
    else:
        form = StaffForm(instance=staff)
    return render(request, 'staff/staff_update.html', {'form': form})



def staff_delete(request, staff_id):
    staff = get_object_or_404(Staff, pk=staff_id)
    if request.method == 'POST':
        staff.delete()
        messages.success(request, 'Stadd deleted successful')
        return redirect('staff_list')
    return redirect('staff_list')
 

def create_marks(request, student_id):
    mark_forms = []
    student = get_object_or_404(Student, id=student_id)
    student_standard = student.standard
    last_test = Testname.objects.filter(standard=student_standard).last()

    if request.method == 'POST':
        test_form = TestSelectionForm(request.POST, student=student)
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
                    mark.subject = Testsubject.objects.get(id=int(mf.prefix))
                    mark.status = mf.initial.get('status')
                    mark.save()
                messages.success(request, 'Mark added successful')
                return redirect('student_detail', student_id=student_id)

            else:
                print("Mark forms errors:", [mf.errors for mf in mark_forms])
        else:
            print("Test form errors:", test_form.errors)
    else:
        test_form = TestSelectionForm(initial={'student': student, 'test': last_test}, student=student)
        subjects = Testsubject.objects.filter(test_name=last_test)
        mark_forms = [MarkForm(prefix=str(subject.id), subject=subject) for subject in subjects]
    
    return render(request, 'subject_standard/mark_form.html', {
        'test_form': test_form,
        'mark_forms': mark_forms,
    })




def get_subjects(request):
    test_id = request.GET.get('test')
    subjects = Testsubject.objects.filter(test_name_id=test_id)
    subject_data = [{'id': subject.id, 'subject': str(subject.subject)} for subject in subjects]
    return JsonResponse({'subjects': subject_data})


def update_mark(request, mark_id):
    mark = get_object_or_404(Mark, pk=mark_id)
    student = mark.student
    test = mark.test
    test_subject = mark.subject

    if request.method == 'POST':
        form = MarkFormupdate(request.POST, instance=mark, total_mark=test_subject.total_mark, pass_mark=test_subject.pass_mark)
        if form.is_valid():
            form.save()
            messages.success(request, 'Mark updated successful')
            return redirect('student_detail', student_id=student.id)
        else:
            print(form.errors)  
    else:
        form = MarkFormupdate(instance=mark, total_mark=test_subject.total_mark, pass_mark=test_subject.pass_mark)

    return render(request, 'subject_standard/mark_update.html', { 'form': form, 'student': student, 'test': test,  'mark': mark,})



def mark_delete(request, id):
    mark = get_object_or_404(Mark, id=id)
    student_id = mark.student.id
    if request.method == 'POST':
        mark.delete()
        messages.success(request, 'Mark deleted successful')
        return redirect('student_detail', student_id=student_id)

    return redirect('student_detail', student_id=student_id)

 
