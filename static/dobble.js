namespace = "/dobble";
var socket = io(namespace);

var game_id = parseInt(window.location.pathname.replace(/^\/+|\/+$/g, ''));
var cycle_id;

var connected = false;

var animation_running = false;

socket.on("connect", function() {
    var background = document.body.style.background;
    socket.emit("client_connect", {"background": background, "game_id": game_id});
    connected = true;
});

socket.on("bad_link", function() {
    window.location.href = "/";
});

function connected_and_ready() {
    if(connected === false) {
       window.setTimeout(connected_and_ready, 100);
    } else {
      socket.emit("client_ready", {});
    }
}

var Imgs = {};
function doc_ready() {
    var imgs_elm = document.getElementById("img_container").children;
    for (var i=0; i < imgs_elm.length; i++){
        Imgs[i] = imgs_elm[i].src;
    }
    connected_and_ready();
};

function make_deck (card, id) {
    var new_deck = document.createElement("div");
    new_deck.className ="deck";
    new_deck.id = id;
    var index = 0;
    for (var pict_id in card){
        var new_deck_elm = document.createElement("img");

        new_deck_elm.src = Imgs[pict_id];
        new_deck_elm.style.left = card[pict_id].x + "%";
        new_deck_elm.style.top = card[pict_id].y + "%";
        new_deck_elm.style.height = card[pict_id].h + "%";
        new_deck_elm.style.transform = "translate(-50%, -50%) rotate("+card[pict_id].r+"deg)";
        if (id == "player_deck") {
            new_deck_elm.addEventListener("click", pict_clicked.bind(this, pict_id));
            new_deck_elm.className = "clickable";
        }
        new_deck_elm.draggable = false;
        new_deck.appendChild(new_deck_elm);
        index++;
    }
    return new_deck;
};

var firstcard = true;
socket.on("move_result", function(data) {

    var body = document.body;

    var player_card = data["player_card"];
    var common_card = data["common_card"];
    var player_deck = document.getElementById("player_deck");
    var common_deck = document.getElementById("common_deck");

    var winner_case = (!(data["player_card"] === undefined));
    var pos_start = document.getElementById("player_deck").getBoundingClientRect();
    var pos_end = document.getElementById("common_deck").getBoundingClientRect();

    cycle_id = data.cycle_id;
    const anim_time = 300;

    if (!firstcard) {
        animation_running = true;
        if (winner_case) {
            pos_start = (pos_start.y-9)+"px";
            deck_temp = player_deck.cloneNode(true);
            setTimeout(()=> common_deck.replaceWith(make_deck(common_card, "common_deck")), anim_time);
            player_deck.replaceWith(make_deck(player_card, "player_deck"));

        } else {
            pos_start = (0 - pos_start.height - pos_start.y)+"px";
            deck_temp = make_deck(common_card, "deck_temp");
            setTimeout(()=> common_deck.replaceWith(make_deck(common_card, "common_deck")), anim_time);
        }
        deck_temp.id = "deck_temp";
        deck_temp.style.top = pos_start;

        body.appendChild(deck_temp);
        setTimeout(()=> deck_temp.style.top = pos_end.y-9+"px", 10);
        setTimeout(()=> deck_temp.remove(), anim_time);
        setTimeout(()=> animation_running = false, anim_time)
    }
    else {
        player_deck.replaceWith(make_deck(player_card, "player_deck"));
        common_deck.replaceWith(make_deck(common_card, "common_deck"));
    }

    firstcard = false;
});

function pict_clicked(pict_id) {
    if (!animation_running) {
        socket.emit("pict_clicked", {"pict_id": pict_id, "game_id": game_id, "cycle_id": cycle_id});
    }
};

socket.on("score", function(data) {

    var score_bar = document.getElementById("score_bar");
    for (var player_color in data) {
        var score_indicator = document.getElementById(player_color);
        if (score_indicator == null) {
            score_indicator = document.createElement("div");
            score_indicator.id = player_color;
            score_indicator.style.background = player_color;
            score_indicator.className = "score";
            score_bar.appendChild(score_indicator);
        }
        score_indicator.style.width = data[player_color]+"%";
    }

    var score_indicators = document.getElementById("score_bar").children;
    var index = 0;
    for (var score_indicator in score_indicators) {
        if (typeof score_indicators[index] === "object") {
            if (!(score_indicators[index].id in data)) {
                var old_player = document.getElementById(score_indicators[index].id);
                old_player.remove();
            }
        }
        index++
    }
});
