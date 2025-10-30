from django.db import models


class Users(models.Model):
    rol = [
    ("Админ", "Админ"),
    ("Модератор", "Модератор"),
    ("Обычный пользователь", "Обычный пользователь")
]
    
    user_name = models.CharField(verbose_name='имя пользователя', max_length=30)
    email = models.EmailField("Почта", max_length=100)
    hash_particle = models.CharField('Хэш', max_length=100)
    registration_date = models.DateField("Дата регистрации")
    about = models.TextField("Информация о себе", null=True, blank=True)
    avatar = models.ImageField('Автарка', upload_to='users_photos/', null=True, blank=True)
    nickname = models.CharField("Никнейм", max_length=50)
    roles = models.CharField('Роль', max_length=50, choices=rol)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        

    
    def __str__(self):
        return f"{self.user_name}"



    
class Donations(models.Model):
    amount = models.DecimalField(verbose_name='сумма', max_digits=7, decimal_places=2) #88888.00
    id_users_from = models.ForeignKey(Users, on_delete=models.SET_NULL, null=True, blank=True, related_name='two', verbose_name='Кто задонатил')
    id_users_to = models.ForeignKey(Users, on_delete=models.SET_NULL, null=True, blank=True, related_name='One', verbose_name='Кому задонатил')
    requisites = models.CharField('Реквизиты', max_length=24)
    content = models.TextField('Содержание доната', null=True, blank=True)
    date = models.DateField('Дата')

    class Meta:
        verbose_name = "Донат"
        verbose_name_plural = "Донаты"
        

    def __str__(self):
        return f"{self.id_users_from} > {self.id_users_to}"
    



class Level(models.Model):
    lev = [ 
    ("МИНОН", "МИНОН"),
    ("МИНИМИНОН", "МИНИМОНОН"),
    ("КУЛИЧ", "КУЛИЧ"),
    ("МИНЬЁН", "МИНЬЁН")
]

    level = models.IntegerField(verbose_name='Уровень')
    name = models.CharField('Название уровня', choices=lev)

    class Meta:
        verbose_name = "Уровень подписки"
        verbose_name_plural = "Уровни подписки"

    def __str__(self):
        return f"{self.id} = {self.name}"
    



class Subscriptions(models.Model):
    id_users_for = models.ForeignKey(Users, on_delete=models.SET_NULL, null=True, blank=True, related_name='three', verbose_name='На кого подписались')
    id_users_from = models.ForeignKey(Users, on_delete=models.SET_NULL, null=True, blank=True, related_name='For', verbose_name='Кто подписался')
    id_level = models.ForeignKey(Level, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Уровень')
    start_date = models.DateField(verbose_name='Дата подписки')
    end_date = models.DateField('Дата отписки', null=True, blank=True)
    auto_renewal = models.BooleanField('Авто продление')

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"

    def __str__(self):
        return f"{self.id_users_from} > {self.id_users_for} = {self.start_date}"



class Streams(models.Model):
    cate = [
    ("IRL", "IRL"),
    ("CREATION", "CREATION"),
    ("ESPORTS", "ESPORTS"),
    ("GAMING", "GAMING"),
    ("MUSIC AND DJS", "MUSIC AND DJS"),
    ("JUST CHATTING", "JUST CHATTING")
]
    status = [
        ("Транслируется", "Транслируется"),
        ("Завершился", "Завершился")
    ]
    
    name = models.CharField('Название стрима', max_length=200)
    id_users = models.ForeignKey(Users, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Пользователь')
    category = models.CharField('Категрия', choices=cate)
    status = models.CharField('Статус', choices=status)
    preview = models.ImageField('Обложка', upload_to='stream-preview/', null=True, blank=True)
    start_time = models.TimeField('Время начала стрима')
    end_time = models.TimeField('Время окончания стрима', null=True, blank=True)
    max_viewers = models.IntegerField('макс. кол. зрителей', null=True, blank=True)


    class Meta:
        verbose_name = "Стрим"
        verbose_name_plural = "Стримы"

    def __str__(self):
        return f"{self.name}"

    @staticmethod
    def get_current_stream():
        return Streams.objects.filter(status="Транслируется").order_by('-id').first()