import django_tables2 as tables
from .models import Person

class PersonTable(tables.Table):
    class Meta:
        model = Person
        template_name = "django_tables2/bootstrap.html"  # Use Bootstrap styling
        fields = ("name", "age", "city")  # Columns to display
