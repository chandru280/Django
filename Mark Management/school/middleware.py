from django.utils.deprecation import MiddlewareMixin
from marks.models import AcademicYear

class AcademicYearMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if 'selected_academic_year' not in request.session:
            latest_year = AcademicYear.objects.last()
            if latest_year:
                request.session['selected_academic_year'] = latest_year.year
