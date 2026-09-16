from django.db import models

# Create your models here.

class Dictionary(models.Model):
    """Справочник"""
    code = models.CharField(
        max_length=100, 
        unique=True, 
        verbose_name="Код"
    )
    name = models.CharField(
        max_length=300, 
        verbose_name="Наименование"
    )
    description = models.TextField(
        blank=True, 
        null=True, 
        verbose_name="Описание"
    )

    class Meta:
        verbose_name = "Справочник"
        verbose_name_plural = "Справочники"
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.code})"


class DictionaryVersion(models.Model):
    """Версия справочника"""
    dictionary = models.ForeignKey(
        Dictionary,
        on_delete=models.CASCADE,
        related_name='versions',
        verbose_name="Справочник"
    )
    version = models.CharField(
        max_length=50, 
        verbose_name="Версия"
    )
    start_date = models.DateField(
        blank=True, 
        null=True, 
        verbose_name="Дата начала действия версии"
    )

    class Meta:
        verbose_name = "Версия справочника"
        verbose_name_plural = "Версии справочников"
        unique_together = ('dictionary', 'version')
        ordering = ['-start_date', 'version']

    def __str__(self):
        return f"{self.dictionary.name} - Версия {self.version}"


class DictionaryElement(models.Model):
    """Элемент справочника"""
    version = models.ForeignKey(
        DictionaryVersion,
        on_delete=models.CASCADE,
        related_name='elements',
        verbose_name="Версия справочника"
    )
    code = models.CharField(
        max_length=100, 
        verbose_name="Код элемента"
    )
    value = models.CharField(
        max_length=300, 
        verbose_name="Значение элемента"
    )

    class Meta:
        verbose_name = "Элемент справочника"
        verbose_name_plural = "Элементы справочника"
        unique_together = ('version', 'code')
        ordering = ['code']

    def __str__(self):
        return f"[{self.code}] {self.value}"
