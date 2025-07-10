from django.db import models  # noqa F401
from django.utils import timezone

class Pokemon(models.Model):
    title = models.CharField(verbose_name='Имя покемона', max_length=200, blank=False )
    photo = models.ImageField(verbose_name='Фото',upload_to="pokemon_images/", blank=True, null=True )
    description = models.TextField(verbose_name='Описание',blank = True, null = True)
    jap_eng_title = models.CharField(verbose_name='Японо-Английское имя',max_length=200, blank = True, null = True)
    evolution = models.ForeignKey("self", verbose_name='Эволюция', on_delete=models.SET_NULL, blank=True, null=True, related_name='evolutions')

    def __str__(self):
        return '{}'.format(self.title)


class PokemonEntity(models.Model):
    lat = models.FloatField(verbose_name='Широта', blank=False )
    lon = models.FloatField(verbose_name='Долгота', blank=False )
    appeared_at = models.DateTimeField(verbose_name='Появление', blank=False )
    disappeared_at = models.DateTimeField(verbose_name='Исчезновение', blank=False)
    pokemon = models.ForeignKey(Pokemon, verbose_name='Покемон', on_delete=models.CASCADE)
    level = models.IntegerField(verbose_name='Уровень',blank=True, null=True)
    health = models.IntegerField(verbose_name='Здоровье',blank=True, null=True)
    strength = models.IntegerField(verbose_name='Сила',blank=True, null=True)
    defence = models.IntegerField(verbose_name='Защита',blank=True, null=True)
    stamina = models.IntegerField(verbose_name='Выносливость',blank=True, null=True)