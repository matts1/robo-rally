$(function() {
    var url = "http://" + document.location.host;
    var csrf = $("input[name=csrfmiddlewaretoken]").val();
    var socket = io.connect(async_url);

    var toTitleCase = function (str) {
        return str.replace(/\w\S*/g, function(txt){return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();});
    }

    var checkLeader = function (data) {
        if (data.text == $("#username").text().toLowerCase() && $("#startgamebutton").length == 0) {
            $("#content").append("<button type='button' id='startgamebutton'>Start Game</button>")
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

    var functions = {
        "adduser": addPlayer,
        "deleteuser": removePlayer,
    }

    var send = function (action, msg) {
        data = {
            "csrfmiddlewaretoken" : csrf,
            "action": action,
            "text": msg,
        };
        console.log("sending", action, "msg is", msg);
        $.post(url + "/send/", data, function (data) {
            console.log("Data status:", data.status);
        }, "json");
    }

    var disconnected = function() {
        setTimeout(start, 1000);
    };

    var messaged = function(data) {
        var i = data.indexOf("\n");
        var action = data.slice(0, i);
        var msg = data.slice(i + 1);
        functions[action](msg);
    };

    socket.on("message", function (data) {
        console.log(data.data.action, data.data.user, data.data.text);
        functions[data.data.action](data.data)
    });

    socket.send($("#username").text());

    $("#startgamebutton").click(function() {
        send("goto_pickmap", "");
    })
});
