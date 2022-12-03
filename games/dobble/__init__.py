from os import listdir, path
from flask import request, render_template, redirect
from app import socketio, playing
from .card import Card


@socketio.on('pict_clicked', namespace="/dobble")
def handle_my_custom_event(data):
    if data is not None:
        print('received json: ' + str(data))
        user = request.sid # NOQA
        try:
            game_id = int(data["game_id"])
            playing.games[game_id].on_receive(user, data)
        except KeyError:
            redirect("index")
        except ValueError:
            redirect("index")


class Dobble:
    MAX_PLAYERS = 8

    def __init__(self, theme):
        theme_path = f"static/themes/{theme}"
        imgs_path = listdir(theme_path)
        self.imgs_path = {k: path.join(theme_path, v) for k, v in enumerate(imgs_path) if path.splitext(v)[1] == ".png"}
        self.img_list = list(range(len(imgs_path)))
        self.players = {}
        self.common_card = Card(self.img_list)
        self.cycle_id = 0

    def layout(self):
        return render_template("dobble.html", imgs_path=self.imgs_path)

    def on_connect(self, user):
        self.players[user] = {"card": self.new_card(), "score": 0}

    def on_ready(self, user):
        self.send_cards(user)

    def on_disconnect(self, user):
        self.players.pop(user)

    def on_receive(self, user, data):
        player_card = self.players[user]["card"].picts
        common_card = self.common_card.picts
        common_pict = list(player_card & common_card)[0]
        clicked_pict = int(data["pict_id"])
        cycle_id = data["cycle_id"]

        if cycle_id == self.cycle_id:
            if common_pict == clicked_pict:
                self.cycle_id += 1
                self.players[user]["score"] += 1
                self.common_card = self.players[user]["card"]
                self.players[user]["card"] = self.new_card()
                self.send_cards(user)
                loosers = set(self.players.keys()) - {user}
                if loosers:
                    self.send_cards(*loosers)
            else:
                self.players[user]["score"] -= 1

    def send_cards(self, *users):
        data = {"common_card": self.common_card.arragement,
                "cycle_id": self.cycle_id
                }
        if len(users) == 1:
            winner = users[0]
            data["player_card"] = self.players[winner]["card"].arragement
            socketio.emit("move_result", data, namespace="/dobble", room=[winner])
        elif len(users) > 1:
            for looser in users:
                socketio.emit("move_result", data, namespace="/dobble", room=[looser])

    def new_card(self):
        cards = [self.common_card.picts]
        for player_card in self.players.values():
            cards.append(player_card["card"].picts)
        return Card(self.img_list, cards)
