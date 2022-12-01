namespace = '/dobble';
var socket = io(namespace);
var game_id = parseInt(window.location.pathname.replace(/^\/+|\/+$/g, ''))

socket.on('connect', function() {
    socket.emit('client_connect', {data: 'Connected!', game_id: game_id});
});

socket.on('bad_link', function() {
    window.location.href = '/';
});

socket.on('move_result', function(img_pics) {
    img_pics = img_pics["r_picts"]
    for (let i = 0; i < 30; i++) {
    if (img_pics.includes(i)) {
    document.getElementById(i).style.display = "inline-block";
    }
    else{
    document.getElementById(i).style.display = "None";
        }
    }
});

function pict_clicked(pict_id) {
  socket.emit('pict_clicked', {data: {pict_id: pict_id, move_id: 666}, game_id: game_id})
};
