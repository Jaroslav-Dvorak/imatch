from flask import render_template, request, redirect, url_for
from app import app, socketio, playing
from games.dobble import Dobble


@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        theme = request.form["computer"]
        playing + Dobble(theme)
        return redirect(url_for("game", gamenum=playing.next_game_id-1))

    return render_template("index.html")


@app.route("/<int:gamenum>")
def game(gamenum):
    try:
        return playing.games[gamenum].layout()
    except KeyError:
        return redirect(url_for("index"))


if __name__ == '__main__':
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True, host="0.0.0.0")
