from typing import Tuple, Optional

import time
import socketio


# from app import sio
sio = socketio.Server()
app = socketio.WSGIApp(sio, static_files={
    '/': './public/'
})


SECONDS_TO_FIND_GAME = 10

searching_clients = []
rooms = {}


@sio.event()
def connect(sid, environ):
    print(sid, 'connected')


@sio.event()
def disconnect(sid):
    print(sid, 'disconnected')


def match_two_players() -> Optional[Tuple[int, int]]:
    global searching_clients
    if len(searching_clients) >= 2:
        user_1 = searching_clients.pop(0)
        user_2 = searching_clients.pop(0)
        return user_1, user_2
    else:
        return None


@sio.event()
def find_game(sid, user_data):
    global searching_clients
    global rooms

    user_id = user_data['user_id']
    print(f"user_id = {user_id}")
    if user_id not in searching_clients:
        searching_clients.append(user_id)

    for second in range(SECONDS_TO_FIND_GAME):
        sio.emit('search_count', second, to=sid)
        res = match_two_players()
        if res is not None:
            # got two players
            # user_1, user_2 = res[0], res[1]
            rooms[res] = True
            sio.emit('found_game', {'room_id': 'asasas'})
            return
        time.sleep(1)
    try:
        searching_clients.remove(user_id)
    except ValueError:
        pass

    sio.emit('not_found_game', to=sid)
