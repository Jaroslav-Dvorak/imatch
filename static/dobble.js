namespace = "/dobble";
var socket = io(namespace);

var game_id = parseInt(window.location.pathname.replace(/^\/+|\/+$/g, ''));
var cycle_id;

socket.on("connect", function() {
    var background = document.getElementById("body").style.background;
    socket.emit("client_connect", {"background": background, "game_id": game_id});

});

socket.on("bad_link", function() {
    window.location.href = "/";
});

var imgs = {};
function doc_ready() {
    var imgs_elm = document.getElementById("img_container").children;
    for (var i=0; i < imgs_elm.length; i++){
        imgs[i] = imgs_elm[i].src;
    }
    socket.emit("client_ready", {});
}

var firstcard = true;
socket.on("move_result", function(data) {

    var winner = (!(data["player_card"] === undefined));

    cycle_id = data.cycle_id;
    var card = data.common_card;
    var deck_elm = document.getElementById("common_deck").children;
    var index = 0;
    for (var pict_id in card){
        deck_elm[index].src = imgs[pict_id];
        deck_elm[index].style.left = card[pict_id].x + "%";
        deck_elm[index].style.top = card[pict_id].y + "%";
        deck_elm[index].style.height = card[pict_id].h + "%";
        deck_elm[index].style.transform = "translate(-50%, -50%) rotate("+card[pict_id].r+"deg)";
        index++
    }
    var card = data.player_card;
    var deck_elm = document.getElementById("player_deck").children;
    var index = 0;
    for (var pict_id in card){
        deck_elm[index].src = imgs[pict_id];
        deck_elm[index].style.left = card[pict_id].x + "%";
        deck_elm[index].style.top = card[pict_id].y + "%";
        deck_elm[index].style.height = card[pict_id].h + "%";
        deck_elm[index].style.transform = "translate(-50%, -50%) rotate("+card[pict_id].r+"deg)";
        deck_elm[index].replaceWith(deck_elm[index].cloneNode(true));
        deck_elm[index].addEventListener("click", pict_clicked.bind(this, pict_id));
        index++
    }
});

function btn_clicked() {
    var deck_elm = document.getElementById("player_deck")
    var pos_start = deck_elm.getBoundingClientRect();
    var temp_deck = deck_elm.cloneNode(true)
    var deck_elm = document.getElementById("common_deck")
    var pos_end = deck_elm.getBoundingClientRect();
    temp_deck.id = "temp_player_deck"
    temp_deck.style.position = "fixed";
    temp_deck.style.transition = "top 0.2s ease-out 0s";
    temp_deck.style.top = pos_start.y-10+"px";
    var body = document.getElementById("body");
    body.appendChild(temp_deck);
    var temp_deck = document.getElementById("temp_player_deck")
    setTimeout(()=> temp_deck.style.top = pos_end.y-10+"px", 1);
}

function pict_clicked(pict_id) {
    socket.emit("pict_clicked", {"pict_id": pict_id, "game_id": game_id, "cycle_id": cycle_id});
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
