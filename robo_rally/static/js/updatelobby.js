document.ready = function() {
    window.url = "http://" + document.location.host;
    window.username = $("#username").text();
    window.csrf = $("input[name=csrfmiddlewaretoken]").val();
    window.socket = io.connect(async_url);
    window.socket.send(username);

    window.socket.on("message", function (data) {
        console.log("receiving", data.data.action, data.data.user, data.data.text);
        functions[data.data.action](data.data)
    });

    if ($("#loadmaplist").length) {
        gotoPickMap(undefined);
    }

    $("#startgamebutton").click(function() {
        send("goto_pickmap", "");
    });
};

var toTitleCase = function (str) {
    return str.replace(/\w\S*/g, function(txt){return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();});
}

var checkLeader = function (data) {
    if (data.text == username.toLowerCase() && $("ul#playerlist li").length > 1) {
        $("#startgamebutton").removeClass("invisible");
    } else {
        $("#startgamebutton").addClass("invisible");
    }
}

var addPlayer = function (data) {
    player = data.user;
    removePlayer(data);
    $("#playerlist").append("<li>" + toTitleCase(player) + "</li>");
    checkLeader(data);
}

var removePlayer = function (data) {
    $("#playerlist li").filter(function() {
        return data.user.toLowerCase() == $(this).text().toLowerCase();
    }).remove();
    // show the button if we are the new leader
    checkLeader(data);
}

var gotoPickMap = function (data) {
    $("#playerlist").appendTo($("#content"));
    $("#dynamic_element").load("/pickmap/" + $("#playerlist li").length, function () {
        initMagicTable();
    });
}

var startGame = function (data) {
    $("#dynamic_element").load("/playgame/", function () {
        loadBoard("a", "b"); // change these arguments
    });
}

var functions = {
    "adduser": addPlayer,
    "deleteuser": removePlayer,
    "goto_pickmap": gotoPickMap,
    "startgame": startGame,
}

var send = function (action, msg) {
    data = {
        "csrfmiddlewaretoken" : csrf,
        "action": action,
        "text": msg,
    };
    if (action != "ping") {
        console.log("sending", action, "msg is", msg);
    }
    $.post(url + "/send/", data, "json");
}

setInterval(function() { // ping every 10 seconds
   send("ping", "");
}, 10000);
