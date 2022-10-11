import logging
from concurrent.futures import ThreadPoolExecutor, as_completed

from django.db import connections
from django.http.response import JsonResponse

from .models import Game, Player

logger = logging.getLogger(__name__)


def index(request):
    def on_done(future):
        connections.close_all()

    def create():
        white_player, _ = Player.objects.get_or_create(name='Grischuk')
        black_player, _ = Player.objects.get_or_create(name='Le Quang Liem')
        game = Game.objects.create(white_player=white_player, black_player=black_player, result=-1)
        return game

    with ThreadPoolExecutor() as executor:
        futures = []
        for _ in range(10_000):
            future = executor.submit(create)
            future.add_done_callback(on_done)
            futures.append(future)

        for future in as_completed(futures):
            logger.error(future.result())

    return JsonResponse({'success': True})
