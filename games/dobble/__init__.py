from os import listdir, path
from flask import request, render_template, redirect
from app import socketio, playing
from .card import Card


@socketio.on('pict_clicked', namespace="/dobble")
def handle_my_custom_event(data):
    if data is not None:
        print('received json: ' + str(data))
        user = request.sid
        try:
            game_id = int(data["game_id"])
            playing.games[game_id].on_receive(user, data)
        except KeyError:
            redirect("index")
        except ValueError:
            redirect("index")


class Dobble:
    def __init__(self, theme):
        theme_path = f"static/themes/{theme}"
        imgs_path = listdir(theme_path)
        self.imgs_path = {k: path.join(theme_path, v) for k, v in enumerate(imgs_path) if path.splitext(v)[1] == ".png"}
        self.img_list = list(range(len(imgs_path)))
        self.players = set()

        self.cards = [Card(self.img_list)]

    def layout(self):
        return render_template("dobble.html", imgs_path=self.imgs_path)

    def on_connect(self, user):
        self.players.add(user)

    def on_disconnect(self, user):
        self.players.remove(user)

    def on_receive(self, user, data):
        self.send_data({})

    def send_data(self, data):

        card = Card(self.img_list)

        socketio.emit("move_result", card.arragement, namespace="/dobble")

