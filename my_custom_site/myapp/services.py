def fetch_custom_data(keyword):
    from django.db import connection
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM myapp_custommodel WHERE title LIKE %S", [f'%{keyword}%'])
        return cursor.fetchall()