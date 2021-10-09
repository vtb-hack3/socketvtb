function getRandomInt(max) {
  return Math.floor(Math.random() * max);
}

const sio = io();

sio.on('connect', () => {
  console.log('connected');
  // sio.emit('find_game', {'user_id': 3})
  console.log('started game');
  sio.emit('find_game', {'user_id': getRandomInt(100)})
});

sio.on('disconnect', () => {
  console.log('disconnected');
});

sio.on('search_count', (count) => {
  console.log(10 - count + ' seconds left.');
});

sio.on('found_game', (data) => {
  console.log('game id: ' + data['room_id']);
});

sio.on('not_found_game', () => {
  console.log('Game was not found');
});