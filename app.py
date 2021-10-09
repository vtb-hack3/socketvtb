import socketio


sio = socketio.Server()
app = socketio.WSGIApp(sio, static_files={
    '/': './public/'
})

#
# app = socketio.WSGIApp(sio, static_files={
#     '/': './public/'
# })
