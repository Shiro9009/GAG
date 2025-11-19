from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Users(models.Model):
    rol = [
        ("Админ", "Админ"),
        ("Модератор", "Модератор"),
        ("Обычный пользователь", "Обычный пользователь")
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь Django', null=True, blank=True)
    user_name = models.CharField(verbose_name='Имя пользователя', max_length=30, default="Пользователь")
    email = models.EmailField("Почта", max_length=100, default="user@example.com")
    hash_particle = models.CharField('Хэш', max_length=100, blank=True, null=True)
    registration_date = models.DateField("Дата регистрации", auto_now_add=True)
    about = models.TextField("Информация о себе", null=True, blank=True)
    avatar = models.ImageField('Аватарка', upload_to='users_photos/', null=True, blank=True, default='users_photos/default_avatar.png')
    nickname = models.CharField("Никнейм", max_length=50, default="User")
    roles = models.CharField('Роль', max_length=50, choices=rol, default="Обычный пользователь")

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return f"{self.nickname}"

class Donations(models.Model):
    amount = models.DecimalField(verbose_name='Сумма', max_digits=7, decimal_places=2, default=0)
    id_users_from = models.ForeignKey(Users, on_delete=models.SET_NULL, null=True, blank=True, related_name='sent_donations', verbose_name='Кто задонатил')
    id_users_to = models.ForeignKey(Users, on_delete=models.SET_NULL, null=True, blank=True, related_name='received_donations', verbose_name='Кому задонатил')
    requisites = models.CharField('Реквизиты', max_length=24, default="")
    content = models.TextField('Содержание доната', null=True, blank=True)
    date = models.DateField('Дата', auto_now_add=True)

    class Meta:
        verbose_name = "Донат"
        verbose_name_plural = "Донаты"

    def __str__(self):
        return f"{self.id_users_from} > {self.id_users_to} - {self.amount}"

class Level(models.Model):
    lev = [ 
        ("МИНОН", "МИНОН"),
        ("МИНИМИНОН", "МИНИМОНОН"),
        ("КУЛИЧ", "КУЛИЧ"),
        ("МИНЬЁН", "МИНЬЁН")
    ]

    level = models.IntegerField(verbose_name='Уровень', default=1)
    name = models.CharField('Название уровня', max_length=50, choices=lev, default="МИНОН")

    class Meta:
        verbose_name = "Уровень подписки"
        verbose_name_plural = "Уровни подписки"

    def __str__(self):
        return f"{self.level} - {self.name}"

class Subscriptions(models.Model):
    id_users_for = models.ForeignKey(Users, on_delete=models.SET_NULL, null=True, blank=True, related_name='subscribers', verbose_name='На кого подписались')
    id_users_from = models.ForeignKey(Users, on_delete=models.SET_NULL, null=True, blank=True, related_name='subscriptions', verbose_name='Кто подписался')
    id_level = models.ForeignKey(Level, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Уровень')
    start_date = models.DateField(verbose_name='Дата подписки', auto_now_add=True)
    end_date = models.DateField('Дата отписки', null=True, blank=True)
    auto_renewal = models.BooleanField('Авто продление', default=True)

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"

    def __str__(self):
        return f"{self.id_users_from} > {self.id_users_for}"


class StreamCategory(models.Model):
    name = models.CharField('Название категории', max_length=50,  unique=True)
    image = models.ImageField('Изображение категории', upload_to='category_images/', null=True, blank=True)
    description = models.TextField('Описание категории', null=True, blank=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    current_viewers = models.IntegerField('Текущее количество зрителей', default=0)
    total_streams = models.IntegerField('Всего стримов', default=0)
    
    class Meta:
        verbose_name = "Категория стримов"
        verbose_name_plural = "Категории стримов"
    
    def __str__(self):
        return self.name
    
    def update_statistics(self):
        """Обновление статистики категории"""
        active_streams = Streams.objects.filter(category=self, status="Транслируется")
        self.total_streams = Streams.objects.filter(category=self).count()
        self.current_viewers = sum(stream.max_viewers or 0 for stream in active_streams)
        self.save()

class Streams(models.Model):
    status = [
        ("Транслируется", "Транслируется"),
        ("Завершился", "Завершился")
    ]
    
    name = models.CharField('Название стрима', max_length=200, default="Новый стрим")
    id_users = models.ForeignKey(Users, on_delete=models.CASCADE, verbose_name='Пользователь')
    category = models.ForeignKey(StreamCategory, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Категория')
    status = models.CharField('Статус', max_length=50, choices=status, default="Транслируется")
    preview = models.ImageField('Обложка', upload_to='stream-preview/', null=True, blank=True)
    start_time = models.DateTimeField('Время начала стрима', default=timezone.now)
    end_time = models.DateTimeField('Время окончания стрима', null=True, blank=True)
    max_viewers = models.IntegerField('Макс. кол. зрителей', null=True, blank=True, default=0)
    description = models.TextField('Описание стрима', null=True, blank=True)

    class Meta:
        verbose_name = "Стрим"
        verbose_name_plural = "Стримы"

    def __str__(self):
        return f"{self.name} - {self.id_users.nickname}"

    @property
    def is_live(self):
        return self.status == "Транслируется"

    @staticmethod
    def get_current_streams():
        return Streams.objects.filter(status="Транслируется").order_by('-start_time')

    @staticmethod
    def get_current_stream():
        return Streams.objects.filter(status="Транслируется").order_by('-start_time').first()
    
    def save(self, *args, **kwargs):
        # Если категория указана как строка, находим соответствующий объект
        if isinstance(self.category, str):
            try:
                category_obj = StreamCategory.objects.get(name=self.category)
                self.category = category_obj
            except StreamCategory.DoesNotExist:
                pass
        
        super().save(*args, **kwargs)
        if self.category:
            self.category.update_statistics()