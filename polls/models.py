from django.db import models


class Poll(models.Model):
    name = models.CharField(max_length=128)
    start_date = models.DateField(auto_now=True)
    end_date = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-start_date']

    def __str__(self):
        return f'{self.start_date}: {self.name}'


class Question(models.Model):

    FORMATS = [
        ('open', 'open'),
        ('one', 'one'),
        ('many', 'many'),
    ]

    type_question = models.CharField(
        max_length=4,
        choices=FORMATS,
        default='open',
    )
    poll = models.ForeignKey(
        Poll,
        on_delete=models.CASCADE,
        related_name='questions')
    text = models.CharField(max_length=256)

    def __str__(self):
        return f'{self.poll}: {self.text}'


class Variant(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='variants')
    text = models.CharField(max_length=128)

    def __str__(self):
        return f'{self.question.id} {self.text}'


class Answer(models.Model):
    user_poll_id = models.IntegerField()
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='answers')
    answer = models.CharField(max_length=128)

    def __str__(self):
        return f'{self.user_poll_id}: {self.answer}'
