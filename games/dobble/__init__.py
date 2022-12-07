from os import listdir, path
from random import choice
from time import time
from flask import request, render_template, redirect
from app import socketio, playing
from .card import Card
from .player import Player


@socketio.on('pict_clicked', namespace="/dobble")
def handle_my_custom_event(data):
    if data is not None:
        # print('received json: ' + str(data))
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
    COLORS = {"rgb(34, 34, 70)", "rgb(84, 139, 84)", "rgb(139, 35, 35)", "rgb(49, 169, 196)",
              "rgb(81, 46, 95)", "rgb(106, 87, 9)", "rgb(78, 52, 52)", "rgb(227, 94, 79)"}
    # burlywood, darkslategrey, dimgrey, maroon, teal

    def __init__(self, theme):
        theme_path = f"static/themes/{theme}"
        imgs_path = listdir(theme_path)
        self.imgs_path = {k: path.join(theme_path, v) for k, v in enumerate(imgs_path) if path.splitext(v)[1] == ".png"}
        self.img_list = list(range(len(imgs_path)))
        self.players = {}
        self.common_card = Card(self.img_list)
        self.cycle_id = 0
        self.last_win_time = time()

    def layout(self, game_id):
        used_colors = self.COLORS - set([p.color for p in self.players.values()])
        color = choice(list(used_colors))
        return render_template("dobble.html",
                               game_id=game_id, imgs_path=self.imgs_path, background=color)

    def on_connect(self, user, data):
        background = data["background"]
        self.players[user] = Player(self.new_card(), background)

    def on_ready(self, user):
        self.send_cards(user, both_cards=True)

        for usr, obj in self.players.items():
            obj.multiplay_score = 0
        self.send_scores()

    def on_disconnect(self, user):
        self.players.pop(user)
        self.send_scores()

    def on_receive(self, user, data):
        player_card = self.players[user].card.picts
        common_card = self.common_card.picts
        common_pict = list(player_card & common_card)[0]
        clicked_pict = int(data["pict_id"])
        cycle_id = data["cycle_id"]

        if cycle_id == self.cycle_id:
            if common_pict == clicked_pict:
                self.players[user].play(+1)
                self.cycle_id += 1
                self.last_win_time = time()
                self.players[user].score += 1
                self.common_card = self.players[user].card
                self.players[user].card = self.new_card()
                self.send_cards(user, both_cards=True)
                loosers = set(self.players.keys()) - {user}
                if loosers:
                    self.send_cards(*loosers, both_cards=False)
            elif (time() - self.last_win_time) > 0.25:
                self.players[user].play(-1)
            self.send_scores()

    def send_cards(self, *users, both_cards):
        data = {"common_card": self.common_card.arragement,
                "cycle_id": self.cycle_id
                }
        if both_cards:
            winner = users[0]
            data["player_card"] = self.players[winner].card.arragement
            socketio.emit("move_result", data, namespace="/dobble", room=[winner])
        else:
            for looser in users:
                socketio.emit("move_result", data, namespace="/dobble", room=[looser])

    def send_scores(self):
        data = {}
        num_of_players = len(self.players)
        if num_of_players > 1:
            color_scores = {p_obj.color: p_obj.multiplay_score for p_obj in self.players.values()}
            score_combined = sum([score for score in color_scores.values()])

            if score_combined:
                for color, score in color_scores.items():
                    percent = (score / score_combined) * 100
                    data[color] = percent
            else:
                percent = 100/num_of_players
                for color, score in color_scores.items():
                    data[color] = percent

        else:
            for player_obj in self.players.values():
                data[player_obj.color] = player_obj.percentage()
                break

        socketio.emit("score", data, namespace="/dobble")

    def new_card(self):
        cards = [self.common_card.picts]
        for player_card in self.players.values():
            cards.append(player_card.card.picts)
        return Card(self.img_list, cards)



































