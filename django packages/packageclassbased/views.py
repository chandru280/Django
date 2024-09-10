from django_tables2 import SingleTableView
from packageapp.models import Person
from packageapp.tables import PersonTable

class PersonListView(SingleTableView):
    model = Person  # The model from which the data is fetched
    table_class = PersonTable  # The table class to be used
    template_name = 'personal_list.html'  # The template to render
    paginate_by = 10  # Pagination: 10 records per page

    # Optionally, if you need to override the default queryset:
    # def get_queryset(self):
    #     return Person.objects.filter(active=True)  # Add any custom filtering
