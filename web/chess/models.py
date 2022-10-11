from django.db import models


class Player(models.Model):
    name = models.CharField(max_length=254)

    def __str__(self):
        return self.name


class Game(models.Model):
    white_player = models.ForeignKey(Player, on_delete=models.SET_NULL, null=True, related_name='white_games')
    black_player = models.ForeignKey(Player, on_delete=models.SET_NULL, null=True, related_name='black_games')
    result = models.SmallIntegerField()

    def __str__(self):
        return f'({self.pk}) {self.white_player} vs {self.black_player}: {self.result}'
