namespace = '/dobble';
var socket = io(namespace);
var game_id = parseInt(window.location.pathname.replace(/^\/+|\/+$/g, ''))

socket.on('connect', function() {
    socket.emit('client_connect', {data: 'Connected!', game_id: game_id});
});

socket.on('bad_link', function() {
    window.location.href = '/';
});

var imgs = {};
function doc_ready() {
    var imgs_elm = document.getElementById("img_container").children
    for (var i=0; i < imgs_elm.length; i++){
        imgs[i] = imgs_elm[i].src;
    }
    socket.emit("client_ready", {})
}


socket.on('move_result', function(data) {
    var card = data.common_card
    var deck_elm = document.getElementById("common_deck").children;
    var index = 0;
    for (var pict_id in card){
        deck_elm[index].src = imgs[pict_id]
        deck_elm[index].style.left = card[pict_id].x + "%";
        deck_elm[index].style.top = card[pict_id].y + "%";
        deck_elm[index].style.height = card[pict_id].h + "%";
        deck_elm[index].style.transform = "translate(-50%, -50%) rotate("+card[pict_id].r+"deg)";
        index++
    }
    var card = data.player_card
    var deck_elm = document.getElementById("player_deck").children;
    var index = 0;
    for (var pict_id in card){
        deck_elm[index].src = imgs[pict_id]
        deck_elm[index].style.left = card[pict_id].x + "%";
        deck_elm[index].style.top = card[pict_id].y + "%";
        deck_elm[index].style.height = card[pict_id].h + "%";
        deck_elm[index].style.transform = "translate(-50%, -50%) rotate("+card[pict_id].r+"deg)";
        deck_elm[index].addEventListener("click", pict_clicked.bind(this, pict_id), false);
        index++
    }
});

function pict_clicked(pict_id) {
console.log(pict_id)
  socket.emit('pict_clicked', {data: {pict_id: pict_id, move_id: 666}, game_id: game_id})
};

var common_deck;
var player_deck;
function btn_clicked() {
    socket.emit('pict_clicked', {data: {}, game_id: game_id})
}
