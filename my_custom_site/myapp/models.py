from django.db import models, connection
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver


# Кастомне поле для зберігання тексту у верхньому регістрі
class UpperCaseField(models.TextField):
    """
    Кастомне поле, що автоматично зберігає текст у верхньому регістрі.
    """
    def get_prep_value(self, value):
        if value:
            return str(value).upper()
        return value

    def from_db_value(self, value, expression, connection):
        return str(value).upper() if value else value


# Модель для категорій
class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


# 3. Кастомний менеджер для SQL запитів
class CustomModelManager(models.Manager):
    def fetch_with_custom_query(self, keyword):
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM myapp_custommodel WHERE title LIKE %s", [f'%{keyword}%'])
            return cursor.fetchall()


# Модель CustomModel з кастомним полем, методом підрахунку статистики та SQL запитом
class CustomModel(models.Model):
    """
    Модель із кастомним полем та методом для підрахунку статистики.
    """
    title = UpperCaseField(verbose_name='Title', default="UNTITLED")
    content = models.TextField(verbose_name='Content', null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="custom_models", null=True,
                                 blank=True)
    created_at = models.DateTimeField(auto_now=True)

    objects = CustomModelManager()

    def __str__(self):
        return self.title

    def calculate_statistics(self):
        """
        Метод для підрахунку статистики для контенту:
        - кількість слів
        - кількість символів
        """
        if not self.content:
            return {'words': 0, 'characters': 0}

        words = self.content.split()
        characters = len(self.content)
        return {'words': len(words), 'characters': characters}

    @classmethod
    def fetch_by_custom_sql(cls, keyword):
        """
        Кастомний SQL запит для вибірки за заголовком.
        """
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM myapp_custommodel WHERE title LIKE %s", [f'%{keyword}%'])
            return cursor.fetchall()


# Кастомна модель користувача з додатковими полями
class CustomUser(AbstractUser):
    """
    Модель користувача з додатковим полем phone_number.
    """
    phone_number = models.CharField(max_length=15, blank=True, null=True, verbose_name="Phone Number")

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups'
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_permissions_set',  # змінюємо related_name
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )

    def __str__(self):
        return self.username


# Сигнал для виконання дій після збереження CustomModel
@receiver(post_save, sender=CustomModel)
def after_save_custom_model(sender, instance, created, **kwargs):
    if created:
        print(f"New CustomModel object created with title: {instance.title}")
    else:
        print(f"CustomModel object updated: {instance.title}")

class UpperCaseCharField(models.CharField):
    def get_prep_value(self, value):
        if value:
            return value.upper()
        return value

    def from_db_value(self, value, expression, connection):
        return value.upper() if value else value

