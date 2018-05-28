var socket = io.connect("http://localhost:5000/");
socket.emit('connected','hello there');
socket.on('newshell',function(msg){
     console.log("MESSAGEM NOVA");
    $('#screen').append($('<li>').text(msg));
});


socket.on('shellcmd',function(msg){
    l = msg.split('\n');
    console.log(l);
    for(var i = 0; i < l.length; ++i)
    {
        console.log(i);
        $('#text').append($('<p>').text(l[i]));
    }
    
});

function keydown_cmd(input)
{
    cmd_to_shell = input.value + '\n';
    obj = {messageType:'cmd',content:{"cmd":cmd_to_shell, id:0}};
    socket.emit('shellcmd',obj);
    $('#text').append($('<p>').text(input.value));
    input.value = '';
    return false;
}
