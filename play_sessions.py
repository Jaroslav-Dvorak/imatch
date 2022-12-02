from flask import request


class PlaySessions:
    def __init__(self, socketio):
        self.next_game_id = 1
        self.games = {}     # {game_id: Game()}
        self.players = {}   # {client sid: game_id}

        # @socketio.on('connect', namespace="/dobble")
        # def handle_my_custom_event(data):
        #     print('CONNECTED!: ' + str(data))
        #     if data is not None and data.get("game_id", None):
        #         user = request.sid
        #         game_id = int(data["game_id"])
        #         self.games[game_id].on_connect(user)

        @socketio.on('client_connect', namespace="/dobble")
        def client_connect(data):
            user = request.sid
            print(f'User: {user} connected! Data: {data}')
            # if (data is not None and
            #         data.get("game_id", None) is not None and
            #         type(data["game_id"]) == "int"):
            try:
                game_id = data["game_id"]
                self.games[game_id].on_connect(user)
            except KeyError:
                print(f"Game does not exist.")
                socketio.emit("bad_link", {"msg": "bad_link"}, namespace="/dobble")
            else:
                self.players[user] = game_id

        @socketio.on('client_ready', namespace="/dobble")
        def on_ready(data):
            user = request.sid
            print(f'User: {user} connected! Data: {data}')
            # if (data is not None and
            #         data.get("game_id", None) is not None and
            #         type(data["game_id"]) == "int"):
            try:
                game_id = self.players[user]
                self.games[game_id].on_ready(user)
            except KeyError:
                print(f"Game does not exist.")
                socketio.emit("bad_link", {"msg": "bad_link"}, namespace="/dobble")

        @socketio.on('disconnect', namespace="/dobble")
        def handle_my_custom_event():
            user = request.sid
            print(f'User: {user} disconnected!')
            try:
                game_id = self.players[user]
                self.games[game_id].on_disconnect(user)
            except KeyError:
                print("impossible KeyError")
            else:
                self.players.pop(user)
                if not self.games[game_id].players:
                    self.games.pop(game_id)

    def __add__(self, other):
        self.games[self.next_game_id] = other
        self.next_game_id += 1
