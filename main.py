from flask import render_template, request, redirect, url_for
from app import app, socketio, playing
from games.dobble import Dobble


@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        theme = list(request.form.items())[0][0].split(".")[0]
        playing + Dobble("emoji")
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


# TODO:
# - each player other background        ✅
# - score indicator                     ✅
# - animations
# - more themes                         ✅
# - rules and multiplayer description
# - link to github (and others)
# - readme file, public repo
# - english and czech
# - wsgi and deployement
