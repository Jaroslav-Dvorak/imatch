from flask import render_template, request, redirect, url_for
from app import app, socketio, playing
from games.dobble import Dobble


@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        form_request = request.form

        try:
            game_id = form_request["game_id"]
        except KeyError:
            theme = list(request.form.items())[0][0].split(".")[0]
            playing + Dobble(theme)
            return redirect(url_for("game", gamenum=playing.next_game_id-1))
        else:
            if not form_request["game_id"].isdigit():
                return render_template("index.html")
            return redirect(url_for("game", gamenum=game_id))

    return render_template("index.html")


@app.route("/<int:gamenum>")
def game(gamenum):
    try:
        return playing.games[gamenum].layout(game_id=gamenum)
    except KeyError:
        return redirect(url_for("index"))


if __name__ == '__main__':
    socketio.run(app, debug=False, host="0.0.0.0")
    # socketio.run(app, debug=False, host="0.0.0.0")


# TODO:
# - each player other background        ✅
# - score indicator                     ✅
# - animations                          ✅
# - more themes                         ✅
# - rules and multiplayer description
# - link to github (and others)
# - readme file, public repo            ✅
# - english and czech
# - wsgi and deployeent
