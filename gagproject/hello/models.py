from django.db import models

# Create your models here.

class roles(models.Model):
    role_name = models.CharField(verbose_name='название ролей', max_length=30)

    class Meta:
        verbose_name = "Роль"
        verbose_name_plural = "Роли"

    def __str__(self):
        return f"{self.id} {self.role_name}"


class Users(models.Model):
    user_name = models.CharField(verbose_name='имя пользователя', max_length=30)
    email = models.CharField("Почта", max_length=100)
    hash_particle = models.CharField('Хэш', max_length=100)
    registration_date = models.DateField("Дата регистрации")
    nickname = models.CharField("Никнейм", default="No", max_length=50)
    id_roles = models.ForeignKey(roles, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Роль')

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["id", "user_name"]
        

    constraints = [
            models.UniqueConstraint(
                fields = ["surname", "bio"],
                condition = models.Q(desc = "Жив"),
                name = "unique_surname_bio"
            ),
            ]
    
    def __str__(self):
        return f"{self.id} {self.user_name}"



    
class donations(models.Model):
    amount = models.IntegerField(verbose_name='сумма')
    id_users_from = models.ForeignKey(Users, on_delete=models.SET_NULL, null=True, blank=True, related_name='two', verbose_name='Кто задонатил')
    id_users_to = models.ForeignKey(Users, on_delete=models.SET_NULL, null=True, blank=True, related_name='One', verbose_name='Кому задонатил')
    requisites = models.CharField('Реквизиты', max_length=24)
    date = models.DateField('Дата')

    class Meta:
        verbose_name = "Донат"
        verbose_name_plural = "Донаты"

    def __str__(self):
        return f"{self.id} {self.amount}"
    


class level(models.Model):
    level = models.IntegerField(verbose_name='Уровень')
    name = models.CharField('Название уровня', max_length=50)

    class Meta:
        verbose_name = "Уровень подписки"
        verbose_name_plural = "Уровни подписки"

    def __str__(self):
        return f"{self.id} {self.level}"
    



class subscriptions(models.Model):
    id_users_for = models.ForeignKey(Users, on_delete=models.SET_NULL, null=True, blank=True, related_name='three', verbose_name='На кого подписались')
    id_users_from = models.ForeignKey(Users, on_delete=models.SET_NULL, null=True, blank=True, related_name='For', verbose_name='Кто подписался')
    id_level = models.ForeignKey(level, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Уровень')
    start_date = models.DateField(verbose_name='Дата подписки')
    end_date = models.DateField('Дата отписки')
    auto_renewal = models.BooleanField('Авто продление')

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"

    def __str__(self):
        return f"{self.id} {self.start_date}"



class categories(models.Model):
    name = models.CharField(verbose_name='Название категории', max_length=50)


    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return f"{self.id} {self.name}"
    

class streams(models.Model):
    name = models.CharField('Название стрима', max_length=200)
    id_users = models.ForeignKey(Users, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Пользователь')
    id_category = models.ForeignKey(categories, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Категрия')
    status = models.CharField('Статус', max_length=20)
    start_time = models.TimeField('Время начала стрима')
    end_time = models.TimeField('Время окончания стрима')
    max_viewers = models.IntegerField('макс. кол. зрителей')


    class Meta:
        verbose_name = "Стрим"
        verbose_name_plural = "Стримы"

    def __str__(self):
        return f"{self.id} {self.name}"
    

