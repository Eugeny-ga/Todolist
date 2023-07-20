from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from core.models import User

class DatesModelMixin(models.Model):
    class Meta:
        abstract = True  # Помечаем класс как абстрактный – для него не будет таблички в БД

    created = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)
    updated = models.DateTimeField(verbose_name="Дата последнего обновления", auto_now=True)


class GoalCategory(DatesModelMixin):

    title = models.CharField(verbose_name="Название", max_length=255)
    user = models.ForeignKey(User, verbose_name="Автор", on_delete=models.PROTECT)
    is_deleted = models.BooleanField(verbose_name="Удалена", default=False)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.id:  # Когда объект только создается, у него еще нет id
            self.created = timezone.now()  # проставляем дату создания
        self.updated = timezone.now()  # проставляем дату обновления
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Категория целей'
        verbose_name_plural = 'Категории целей'

        # verbose_name = _("Category") #TODO почему не работает перевод
        # verbose_name_plural = _("Categories")


class GoalStatus(models.IntegerChoices):
    to_do = 1, "К выполнению"
    in_progress = 2, "В процессе"
    done = 3, "Выполнено"
    archived = 4, "Архив"

class GoalPriority(models.IntegerChoices):
    low = 1, "Низкий"
    medium = 2, "Средний"
    high = 3, "Высокий"
    critical = 4, "Критический"


class Goal(DatesModelMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    category = models.ForeignKey(GoalCategory, on_delete=models.PROTECT)
    description = models.TextField(blank=True)
    status = models.PositiveSmallIntegerField(verbose_name="Статус",
                                              choices=GoalStatus.choices, default=GoalStatus.to_do)
    priority = models.PositiveSmallIntegerField(verbose_name="Приоритет",
                                                choices=GoalPriority.choices, default=GoalPriority.medium)
    due_date = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name = 'Цель'
        verbose_name_plural = 'Цели'

        # verbose_name = _("Goal")  #TODO почему не работает перевод
        # verbose_name_plural = _("Goals")


class Comment(DatesModelMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE)
    text = models.TextField()

    class Meta:
        # verbose_name = _('Comment')
        # verbose_name_plural = _('Comments')

        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

