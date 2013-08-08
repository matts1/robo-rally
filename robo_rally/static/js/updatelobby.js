$(function() {
    var url = "http://" + document.location.host;
    var csrf = $("input[name=csrfmiddlewaretoken]").val();
    var socket = io.connect(async_url);

    var toTitleCase = function (str) {
        return str.replace(/\w\S*/g, function(txt){return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();});
    }

    var addPlayer = function (player) {
        removePlayer(player);
        $("#playerlist").append("<li>" + toTitleCase(player) + "</li>");
    }

    var removePlayer = function (player) {
        $("#playerlist li").filter(function() {
            return player.toLowerCase() == $(this).text().toLowerCase();
        }).remove();
    }

    var functions = {
        "add": addPlayer,
    }

    var send = function (action, msg) {
        data = {
            "csrfmiddlewaretoken" : csrf,
            "action": "adduser",
            "text": "bob"
        };
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
        console.log("news is", data);
    });

    send("ping", "");
});
