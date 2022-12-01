namespace = '/dobble';
var socket = io(namespace);
var game_id = parseInt(window.location.pathname.replace(/^\/+|\/+$/g, ''))

socket.on('connect', function() {
    socket.emit('client_connect', {data: 'Connected!', game_id: game_id});
});

socket.on('bad_link', function() {
    window.location.href = '/';
});

socket.on('move_result', function(data) {
    var deck_elm = document.getElementById("common_deck").children;
    var index = 0;
    for (var pict_id in data){
        deck_elm[index].src = imgs[pict_id]
        console.log(data[pict_id].h + "%")
        deck_elm[index].style.left = data[pict_id].x + "%";
        deck_elm[index].style.top = data[pict_id].y + "%";
        deck_elm[index].style.height = data[pict_id].h + "%";
        deck_elm[index].style.transform = "translate(-50%, -50%) rotate("+data[pict_id].r+"deg)";

        index++
    }
});

function pict_clicked(pict_id) {
  socket.emit('pict_clicked', {data: {pict_id: pict_id, move_id: 666}, game_id: game_id})
};

var imgs = {};
function doc_ready() {
    var imgs_elm = document.getElementById("img_container").children
    for (var i=0; i < imgs_elm.length; i++){
        imgs[i] = imgs_elm[i].src;
    }
}

var common_deck;
var player_deck;
function btn_clicked() {
    socket.emit('pict_clicked', {data: {}, game_id: game_id})
}

class Deck{
    constructor(content){
    console.log("kdsfased")
        this.container = document.createElement("div");
        this.container.style.height = "400px";
        this.container.style.width = "400px";
        this.container.style.border = "solid"
        document.body.appendChild(this.container)
    }
}