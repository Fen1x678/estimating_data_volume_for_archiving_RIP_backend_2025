from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, User
from django.db import models


class Algorithm(models.Model):
    STATUS_CHOICES = (
        (1, 'Действует'),
        (2, 'Удалена'),
    )

    name = models.CharField(max_length=100, verbose_name="Название")
    description = models.TextField(max_length=500, verbose_name="Описание",)
    status = models.IntegerField(choices=STATUS_CHOICES, default=1, verbose_name="Статус")
    image = models.ImageField(verbose_name="Фото", blank=True, null=True)

    ratio = models.IntegerField(verbose_name="Коэффициент сжатия")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Алгоритм"
        verbose_name_plural = "Алгоритмы"
        db_table = "algorithms"
        ordering = ("pk",)


class Compression(models.Model):
    STATUS_CHOICES = (
        (1, 'Введён'),
        (2, 'В работе'),
        (3, 'Завершен'),
        (4, 'Отклонен'),
        (5, 'Удален')
    )

    status = models.IntegerField(choices=STATUS_CHOICES, default=1, verbose_name="Статус")
    date_created = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)
    date_formation = models.DateTimeField(verbose_name="Дата формирования", blank=True, null=True)
    date_complete = models.DateTimeField(verbose_name="Дата завершения", blank=True, null=True)

    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name="Создатель", related_name='owner', null=True)
    moderator = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name="Математик", related_name='moderator', blank=True,  null=True)

    # Поле пользователя
    data_type = models.IntegerField(blank=True, null=True)

    # Вычисляемое поле
    volume_after = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return "Сжатие №" + str(self.pk)

    class Meta:
        verbose_name = "Сжатие"
        verbose_name_plural = "Сжатия"
        db_table = "compressions"
        ordering = ('-date_formation', )


class AlgorithmCompression(models.Model):
    pk = models.CompositePrimaryKey("algorithm_id", "compression_id")
    algorithm = models.ForeignKey(Algorithm, on_delete=models.DO_NOTHING)
    compression = models.ForeignKey(Compression, on_delete=models.DO_NOTHING)
    
    # Поле м-м
    volume = models.IntegerField(default=0)

    def __str__(self):
        return "м-м №" + str(self.pk)

    class Meta:
        verbose_name = "м-м"
        verbose_name_plural = "м-м"
        db_table = "algorithm_compression"
        ordering = ('pk', )
