from typing import Tuple, Optional, Dict
from config import r, USERS_SEARCHING_FOR_GAME, get_searching_users, _get_first_el_from_dict, set_searching_users

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


@sio.event()
def find_game(sid, user_data):
    global searching_clients
    global rooms

    user_id = user_data['user_id']
    searching_users: Dict = get_searching_users()
    if len(searching_users) > 0:  # someone already looking for game
        opponent_id, opponent_sid = _get_first_el_from_dict(searching_users)
        set_searching_users({})
        # todo: create room in db
        sio.emit('found_game', {'room_id': 33}, to=sid)
        sio.emit('found_game', {'room_id': 33}, to=opponent_sid)
    else:
        set_searching_users({user_id: sid})

        for second in range(SECONDS_TO_FIND_GAME):
            sio.emit('search_count', {'seconds': second}, to=sid)
            time.sleep(1)
            searching_users: Dict = get_searching_users()
            if len(searching_users) == 0:
                return

        sio.emit('not_found_game', to=sid)
