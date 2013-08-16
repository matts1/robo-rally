document.ready = function() {
    window.url = "http://" + document.location.host;
    window.username = $("#username").text();
    window.csrf = $("input[name=csrfmiddlewaretoken]").val();
    window.socket = io.connect(async_url);
    window.socket.send(username);

    window.socket.on("message", function (data) {
        data = data.data;
        console.log("receiving", data.action, data.user, data.text);
        data.text = data.text.split("\n");
        data.action = data.action.split("\n");
        for (var i = 0; i < data.text.length; i++) {
            functions[data.action[i]](data.text[i], data.user);
        }
    });

    if ($("#loadmaplist").length) {
        gotoPickMap(undefined);
    }

    if ($("#gamerunning").length) {
        startGame(undefined);
    }

    $("#startgamebutton").click(function() {
        send("gotopickmap", "");
    });
};

var toTitleCase = function (str) {
    return str.replace(/\w\S*/g, function(txt){return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();});
}

var checkLeader = function (text) {
    console.log(text, username);
    if (text == username.toLowerCase() && $("ul#playerlist li").length > 1) {
        $("#startgamebutton").removeClass("invisible");
    } else {
        $("#startgamebutton").addClass("invisible");
    }
}

var addPlayer = function (text, player) {
    removePlayer(text, player);
    $("#playerlist").append("<li>" + toTitleCase(player) + "</li>");
    checkLeader(text);
}

var removePlayer = function (text, player) {
    $("#playerlist li").filter(function() {
        return player.toLowerCase() == $(this).text().toLowerCase();
    }).remove();
    // show the button if we are the new leader
    checkLeader(text);
}

var gotoPickMap = function (text, player) {
    $("#playerlist").appendTo($("#content"));
    $("#dynamic_element").load("/pickmap/" + $("#playerlist li").length, function () {
        initMagicTable();
    });
}

jQuery.fn.swapWith = function(to) {
    return this.each(function() {
        var copy_to = to.clone(true);
        var copy_from = $(this).clone(true);
        to.replaceWith(copy_from);
        $(this).replaceWith(copy_to);
    });
};

var startGame = function (text, player) {
    if ($("#dynamic_element #playerlist").length) {
        $("#dynamic_element #playerlist").appendTo($("#content"));
    }
    $("#dynamic_element").load("/playgame/", function () {
        loadBoard($("#boarddisplay"), $("#boarddisplay").attr("data-filename"));

        window.selected = null;
        $(".program_card").on("click", function() {
            card = $(this);
            if (window.selected == null) {
                window.selected = card;
            } else {
                if (card != window.selected) {
                    send(
                        "swapcards",
                        $(".program_card").index(card) + " " + $(".program_card").index(window.selected)
                    );
                    card.swapWith(window.selected);
                }
                window.selected = null;
            }
        });

        $("#ready_button").on("click", function(){
            send(
                "playerready", ""
            )
        });
    });
}

var functions = {
    "adduser": addPlayer,
    "deleteuser": removePlayer,
    "gotopickmap": gotoPickMap,
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
