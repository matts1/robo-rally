document.ready = function() {
    window.url = "http://" + document.location.host;
    window.username = $("#username").text();
    window.csrf = $("input[name=csrfmiddlewaretoken]").val();
    window.socket = io.connect(async_url);
    window.socket.send(username);

    window.socket.on("message", function (data) {
        data = data.data;
        console.log(data.action)
        data.text = data.text.split("\n");
        for (var i = 0; i < data.text.length; i++) {
            functions[data.action](data.text[i], data.user);
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
};

var checkLeader = function (text) {
    if (text == username.toLowerCase() && $("ul#playerlist li").length > 1) {
        $("#startgamebutton").removeClass("invisible");
    } else {
        $("#startgamebutton").addClass("invisible");
    }
};

var addPlayer = function (text, player) {
    removePlayer(text, player);
    $("#playerlist").append("<li>" + toTitleCase(player) + "</li>");
    checkLeader(text);
};

var removePlayer = function (text, player) {
    $("#playerlist li").filter(function() {
        return player.toLowerCase() == $(this).text().toLowerCase();
    }).remove();
    // show the button if we are the new leader
    checkLeader(text);
};

var gotoPickMap = function (text, player) {
    $("#playerlist").appendTo($("#content"));
    $("#dynamic_element").load("/pickmap/" + $("#playerlist li").length, function () {
        initMagicTable();
    });
};

jQuery.fn.swapWith = function(to) {
    return this.each(function() {
        var copy_to = to.clone(true);
        var copy_from = $(this).clone(true);
        to.replaceWith(copy_from);
        $(this).replaceWith(copy_to);
    });
};

var move = function (text, player) {
    moves = text.split(" ");
    for (var i = 0; i < moves.length; i+=5) {
        drawSpecial($(".boarddisplay"), window.squareSize, parseInt(moves[i + 1]),
            parseInt(moves[i]), parseInt(moves[i + 2]),
            parseInt(moves[i + 3]), parseInt(moves[i + 4]), (i+1)*5 == moves.length
        );
    }
};

var setOpacity = function (key, value) {
    if (key in window.specials) {
        window.specials[key].css("opacity", value);
    }
}

var virtualCaller = function (text, player) {
    virtual(window.newest_todo, text);
}

var virtual = function (queue_pos, text) {
    if (queue_pos > window.first_queue) {
        setTimeout(function () {
            virtual(queue_pos, text);
        }, 50);
    } else {
        players = text.split(" ");
        for (var i = 16; i < 24; i++) {
            setOpacity(i, 1);
        }
        for (var i = 0; i < players.length; i++) {
            setOpacity(16 + parseInt(players[i]), 0.5);
        }
    }
}

var health = function (text, player) {
    stats = text.split(' ');
    lives = parseInt(stats[0]);
    $(".lives img").remove();
    for (var i = 0; i < lives; i++) {
        $(".lives").append('<img src="/static/images/sheet/life.png">');
    }
    health = parseInt(stats[1]);
    damage = $(".damage img");
    for (var i = 0; i < 9; i++) {
        token = "damage"
        if (i < health) {token = "health"};
        $(damage[i]).attr("src", "/static/images/sheet/" + token + ".png");
    }
};

var startGame = function (text, player) {
    if ($("#dynamic_element #playerlist").length) {
        $("#dynamic_element #playerlist").appendTo($("#content"));
    }
    $("#dynamic_element").load("/playgame/", function () {
        loadBoard($("#boarddisplay"), $("#boarddisplay").attr("data-filename"));

        window.selected = null;
        $("#dynamic_element").on("click", ".program_card", function() {
            card = $(this);
            if ($(this).hasClass("locked")) {
                return; // only perform action if not locked
            }
            if (window.selected == null) {
                window.selected = card
                card.addClass("program_card_border");
            } else {
                if (card != window.selected) {
                    send(
                        "swapcards",
                        $(".program_card").index(card) + " " + $(".program_card").index(window.selected)
                    );
                    $(".program_card_border").removeClass("program_card_border");
                    card.swapWith(window.selected);
                }
                window.selected = null;
            }
        });

        $("#ready_button").on("click", function(){
            send("playerready", "");
        });

        $("#powerdown").click(function() {
            send("powerdown", "");
        })
    });
};

var deal = function (text, player) {
    if (text == "") {
        $(".program_card").addClass("invisible");
    } else {
        $(".program_card").removeClass("invisible");
    }
    hand = text.split(" ");
    $(".hand .program_card").remove();
    cards = $(".program_card");
    for (var i = 0; i < 5; i++) {
        file = hand[i].split(",")[0];
        priority = parseInt(hand[i].split(",")[1]);
        locked = parseInt(hand[i].split(",")[2]);
        $(cards[i]).attr("src", "/static/images/cards/" + priority + ".png");
        if (locked) {
            $(cards[i]).addClass("locked");
        } else {
            $(cards[i]).removeClass("locked");
        }
    }
    for (var i = 5; i < hand.length; i++) {
        file = hand[i].split(",")[0];
        priority = parseInt(hand[i].split(",")[1]);
        $(".hand").append('<img src="/static/images/cards/' + priority + '.png" class="program_card">');
    }
}

var newobjective = function (text, player) {
    $(".nextflag").html(text);
}

var myAlert = function (text, player) {
    alert(text);
}

var restartGame = function (text, player) {
    alert("Everyone died... You must all suck. Let me make a new game for you.");
    location.reload(true);
}

var functions = {
    "adduser": addPlayer,
    "deleteuser": removePlayer,
    "gotopickmap": gotoPickMap,
    "startgame": startGame,
    "move": move,
    "health": health,
    "dealhand": deal,
    "newobjective": newobjective,
    "alert": myAlert,
    "virtual": virtualCaller,
    "restart": restartGame,
};

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
};

setInterval(function() { // ping every 10 seconds
   send("ping", "");
}, 10000);
