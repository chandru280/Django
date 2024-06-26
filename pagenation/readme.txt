1. Simple Pagination

« first previous Page 2 of 8. next last »

(or)
<!DOCTYPE html>
<html>
<head>
    <title>Item List</title>
</head>
<body>
    <h1>Item List</h1>
    <ul>
        {% for item in page_obj %}
            <li>{{ item.name }}</li>
        {% endfor %}
    </ul>

    <div class="pagination">
        <span class="step-links">
            {% if page_obj.has_previous %}
                <a href="?page={{ page_obj.previous_page_number }}">&lt; previous</a>
            {% endif %}

            {% if page_obj.has_next %}
                <a href="?page={{ page_obj.next_page_number }}">next &gt;</a>
            {% endif %}
        </span>
    </div>
</body>
</html>

< previous next >

2. Numeric Pagination



<!DOCTYPE html>
<html>
<head>
    <title>Item List</title>
</head>
<body>
    <h1>Item List</h1>
    <ul>
        {% for item in page_obj %}
            <li>{{ item.name }}</li>
        {% endfor %}
    </ul>

    <div class="pagination">
        <span class="step-links">
            {% if page_obj.has_previous %}
                <a href="?page=1">&laquo; first</a>
                <a href="?page={{ page_obj.previous_page_number }}">previous</a>
            {% endif %}

            {% for num in page_obj.paginator.page_range %}
                {% if num == page_obj.number %}
                    <span class="current">[{{ num }}]</span>
                {% elif num > page_obj.number|add:'-5' and num < page_obj.number|add:'5' %}
                    <a href="?page={{ num }}">{{ num }}</a>
                {% endif %}
            {% endfor %}

            {% if page_obj.has_next %}
                <a href="?page={{ page_obj.next_page_number }}">next</a>
                <a href="?page={{ page_obj.paginator.num_pages }}">last &raquo;</a>
            {% endif %}
        </span>
    </div>
</body>
</html>

<< first < previous [1] 2 3 4 5 > next >> last.


3. Custom Range Pagination


def item_list(request):
    item_list = Item.objects.all()
    paginator = Paginator(item_list, 10)  # Show 10 items per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Custom range logic
    index = page_obj.number - 1  # Current page index
    max_index = len(paginator.page_range)
    start_index = index - 2 if index >= 2 else 0
    end_index = index + 3 if index <= max_index - 3 else max_index
    page_range = list(paginator.page_range)[start_index:end_index]

    return render(request, 'item_list.html', {'page_obj': page_obj, 'page_range': page_range})




<!DOCTYPE html>
<html>
<head>
    <title>Item List</title>
</head>
<body>
    <h1>Item List</h1>
    <ul>
        {% for item in page_obj %}
            <li>{{ item.name }}</li>
        {% endfor %}
    </ul>

    <div class="pagination">
        <span class="step-links">
            {% if page_obj.has_previous %}
                <a href="?page=1">&laquo; first</a>
                <a href="?page={{ page_obj.previous_page_number }}">previous</a>
            {% endif %}

            {% for num in page_range %}
                {% if num == page_obj.number %}
                    <span class="current">[{{ num }}]</span>
                {% else %}
                    <a href="?page={{ num }}">{{ num }}</a>
                {% endif %}
            {% endfor %}

            {% if page_obj.has_next %}
                <a href="?page={{ page_obj.next_page_number }}">next</a>
                <a href="?page={{ page_obj.paginator.num_pages }}">last &raquo;</a>
            {% endif %}
        </span>
    </div>
</body>
</html>

<< first < previous [1] 2 3 4 5 > next >> last.

4. Infinite Scroll Pagination

from django.http import JsonResponse
def item_list(request):
     item_list = Item.objects.all()
    paginator = Paginator(item_list, 10)  # Show 10 items per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        items_html = render_to_string('items_list.html', {'page_obj': page_obj})
        return JsonResponse({'items_html': items_html})

    return render(request, 'item_list.html', {'page_obj': page_obj})

from django.template.loader import render_to_string





<!DOCTYPE html>
<html>
<head>
    <title>Item List</title>
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <script>
        $(document).ready(function(){
            let page = 1;
            let loading = false;

            $(window).scroll(function() {
                if ($(window).scrollTop() + $(window).height() >= $(document).height() - 100 && !loading) {
                    loading = true;
                    page++;
                    $.ajax({
                        url: '?page=' + page,
                        type: 'get',
                        beforeSend: function() {
                            $('#loading').show();
                        },
                        success: function(data) {
                            if(data.items_html.trim() === "") {
                                $('#loading').hide();
                                $(window).off('scroll');
                            } else {
                                $('#item-list').append(data.items_html);
                                $('#loading').hide();
                                loading = false;
                            }
                        }
                    });
                }
            });
        });
    </script>
</head>
<body>
    <h1>Item List</h1>
    <ul id="item-list">
        {% for item in page_obj %}
    <li>{{ item.name }}</li>
{% endfor %}
    </ul>
    <div id="loading" style="display: none;">Loading...</div>
</body>
</html>



5. Load More Button Pagination




<!DOCTYPE html>
<html>
<head>
    <title>Item List</title>
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <script>
        $(document).ready(function() {
            let page = 1;

            $('#load-more').click(function() {
                page++;
                $.ajax({
                    url: '?page=' + page,
                    type: 'get',
                    beforeSend: function() {
                        $('#load-more').text('Loading...');
                    },
                    success: function(data) {
                        $('#item-list').append(data.items_html);
                        if (!data.has_next) {
                            $('#load-more').hide();
                        } else {
                            $('#load-more').text('Load More');
                        }
                    }
                });
            });
        });
    </script>
</head>
<body>
    <h1>Item List</h1>
    <ul id="item-list">
        {% for item in page_obj %}
    <li>{{ item.name }}</li>
{% endfor %}

    </ul>
    {% if page_obj.has_next %}
        <button id="load-more">Load More</button>
    {% endif %}
</body>
</html>




from django.http import JsonResponse
def item_list(request):
    item_list = Item.objects.all()
    paginator = Paginator(item_list, 10)  # Show 10 items per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        items_html = render_to_string('items_partial.html', {'page_obj': page_obj})
        return JsonResponse({'items_html': items_html, 'has_next': page_obj.has_next()})

    return render(request, 'item_list.html', {'page_obj': page_obj, 'paginator': paginator})

from django.template.loader import render_to_string