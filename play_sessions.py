from flask import request


class PlaySessions:
    def __init__(self, socketio):
        self.next_game_id = 1
        self.games = {}     # {game_id: Game()}
        self.players = {}   # {client sid: game_id}

        @socketio.on('client_connect', namespace="/dobble")
        def client_connect(data):
            user = request.sid # NOQA
            print(f'User: {user} connected! Data: {data}')
            refuse = False
            try:
                game_id = data["game_id"]
                self.games[game_id].on_connect(user)
            except KeyError:
                print(f"On_client: Game does not exist.")
                refuse = True
            else:
                max_players = self.games[game_id].MAX_PLAYERS
                playing = len(self.players)
                if playing < max_players:
                    self.players[user] = game_id
                else:
                    refuse = True
            if refuse:
                socketio.emit("bad_link", {"msg": "bad_link"}, namespace="/dobble")

        @socketio.on('client_ready', namespace="/dobble")
        def on_ready(data):
            user = request.sid # NOQA
            print(f'User: {user} ready! Data: {data}')
            try:
                game_id = self.players[user]
                self.games[game_id].on_ready(user)
            except KeyError:
                print(f"On ready: Game does not exist.")
                socketio.emit("bad_link", {"msg": "bad_link"}, namespace="/dobble")

        @socketio.on('disconnect', namespace="/dobble")
        def disconnect():
            user = request.sid # NOQA
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
