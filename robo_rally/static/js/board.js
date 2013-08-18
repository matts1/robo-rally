var FILES = [
    "doubleconveyerconvergeanticlockwise.png",
    "doubleconveyerconvergeclockwise.png",
    "doubleconveyerconverge.png",
    "doubleconveyerstraight.png",
    "doubleconveyerturnanticlockwise.png",
    "doubleconveyerturnclockwise.png",
    "doublelaser.png",
    "doublepusher.png",
    "empty.png",
    "floor.png",
    "greengear.png",
    "hammerwrench.png",
    "laser.png",
    "pit.png",
    "redgear.png",
    "repair.png",
    "singleconveyerconvergeanticlockwise.png",
    "singleconveyerconvergeclockwise.png",
    "singleconveyerconverge.png",
    "singleconveyerstraight.png",
    "singleconveyerturnanticlockwise.png",
    "singleconveyerturnclockwise.png",
    "singlelaser.png",
    "triplelaser.png",
    "triplepusher.png",
    "wall.png",
]
SIDES = [[0, 0], [1, 0], [0, 1], [0, 0]];

function loadTableRowBoard(obj, url) {
    obj = $(obj);
    obj.toggleClass("rot180");
    tr = obj.parent().parent();
    if ($(".boarddisplay", tr.next()).length) {
        tr.next().toggleClass("invisible");
        return;
    }
    overlay = $("<tr><td class='boardinfo'colspan='5'>"+
        "<div class='description'></div>"+
        "<div class='boarddisplay'></div>"+
        "<div class='rules'></div>"+
    "</td></tr>");
    obj.parent().parent().after(overlay);
    overlay = $("td", overlay);
    loadBoard(overlay, url);
};

function loadBoard(obj, url) {
    window.first_queue = 0;
    window.newest_todo = 0;

    $.get(url, {}, function(data) {
        data = $(data);
        var fields = [
            "name", "description", "rules", "length", "difficulty",
            "minplayers", "maxplayers", "numflags"
        ];
        for (var i = 0; i < fields.length; i++) {
            var field = fields[i];
            if ($("." + field, obj).length > 0) {
                $($("." + field, obj)[0]).html($("." + field, data).html());
            }
        }
        window.specials = {};
        drawBoard($(".boarddisplay", obj), $(".board", data), $(".spawn", data), $(".flags", data));

        locations = $(".loc div");
        for (var i = 0; i < locations.length; i++) {
            text = $(locations[i]).text().split(" ");
            drawSpecial($(".boarddisplay"), window.squareSize,
                parseInt(text[0]), parseInt(text[1])-1,
                parseInt(text[2]), parseInt(text[3]), parseInt(text[4]));
        }
    });
};

function drawBoard(display, board, spawn, flags) {
    display.empty();
    var displayWidth = parseInt(display.css("width"));
    var boardHeight = board.children().length;
    var boardWidth = $(board.children()[0]).children().length;

    var squareSize = Math.min(displayWidth / boardWidth, 46);
    window.squareSize = squareSize;
    display.css("height", squareSize * boardHeight);
    for (var y = 0; y < boardHeight; y++) {
        var row = $(board.children()[y]);
        for (var x = 0; x < boardWidth; x++) {
            var square = $(row.children()[x]).html().split(",");
            var img = new Image();
            img.src = "/static/images/board/" + FILES[parseInt(square[0])];
            display.append(img);
            $(img).addClass("floor");
            $(img).css("height", squareSize);
            $(img).css("width", squareSize);
            $(img).css("top", y * squareSize);
            $(img).css("left", x * squareSize);
            $(img).addClass("rot" + square[1]);
            
            for (var i = 0; i < 4; i++) {
                if (parseInt(square[i + 2]) == 8) continue; // empty
                var img = new Image();
                img.src = "/static/images/board/" + FILES[parseInt(square[i + 2])];
                img.i_tmp = i;
                img.x_tmp = x;
                img.y_tmp = y;
                display.append(img);
                img.onload = function() {
                    var i = this.i_tmp;
                    var x = this.x_tmp;
                    var y = this.y_tmp;
                    img = $(this);
                    img.addClass("side");
                    img.addClass("rot" + (i * 90));
                    img.css("width", squareSize);
                    var imgx = x * squareSize;
                    var imgy = y * squareSize;
                    var height = parseInt(img.css("height"));

                    if (i == 1) {
                        imgx += (squareSize - height) / 2;
                        imgy += (squareSize - height) / 2;
                    } else if (i == 2) {
                        imgy += squareSize - height;
                    } else if (i == 3) {
                        imgx -= (squareSize - height) / 2;
                        imgy += (squareSize - height) / 2;
                    }
                    img.css("left", imgx);
                    img.css("top", imgy);
                }
            }
        }
    }
    flags = flags.html().split(" ");
    spawn = spawn.html().split(" ");
    for (var i = 0; i < flags.length; i++) {
        coords = flags[i].split(",");
        if (coords.length == 2) {
            drawSpecial(display, squareSize, 0, i, parseInt(coords[0]), parseInt(coords[1]), 0);
        }
    }
    for (var i = 0; i < spawn.length; i++) {
        coords = spawn[i].split(",");
        drawSpecial(display, squareSize, 1, i, parseInt(coords[0]), parseInt(coords[1]), 0);
    }
};

function animate (queue_pos, img, new_left, new_top, rot) {
    if (queue_pos != window.first_queue) {
        setTimeout(function () {
            animate(queue_pos, img, new_left, new_top, rot);
        }, 50)
    } else {
        img.stop().animate({
        left: new_left + 'px',
        top: new_top + 'px'},
        {queue: false, duration: 600, complete: function() {
            // console.log("rotating to", rot * 90, "from", img.getRotateAngle()[0]);
//            img.rotate({
//                duration: 1000,
//                angle: img.getRotateAngle()[0],
//                animateTo: rot * 90,
//                callback: function () {
//                    window.first_queue = queue_pos + 1;
//                }
//            });
            img.stop().animate({  borderSpacing: rot * 90 }, {
            step: function(now,fx) {
                $(this).css('-webkit-transform','rotate('+now+'deg)');
                $(this).css('-moz-transform','rotate('+now+'deg)');
                $(this).css('-ms-transform','rotate('+now+'deg)');
                $(this).css('-o-transform','rotate('+now+'deg)');
                $(this).css('transform','rotate('+now+'deg)');
            }, queue: false, duration:'300', complete: function() {
                window.first_queue = queue_pos + 1;
            }});
        }});
    }
}

function drawSpecial(display, squareSize, type, objid, x, y, rot) {
    last = true;
    if (arguments.length > 7) {
        last = arguments[7];
    }
    key = (8 * type) + objid;
    if (x == -1 && y == -1) { // they are dead
        x = y = 9001;
//        if (key in window.specials) {
//            window.specials[key].remove();
//            delete window.specials[key];
//        }
//        return;
    }
    if (key in window.specials && type == 1) { // spawn, don't animate
        window.specials[key].remove();
        delete window.specials[key];
    } else if (key in window.specials) {
        if (window.specials[key] != 1) {
            img = window.specials[key];
            new_left = (x * squareSize) + (squareSize - img.width()) / 2;
            new_top = (y * squareSize) + (squareSize - img.height()) / 2;
            animate(window.newest_todo, img, new_left, new_top, rot);
            if (last) {
                window.newest_todo++;
            }

            if (type == 2) {
                for (var i = 0; i < 4; i++) {
                    img.removeClass("rot" + i*90);
                }
                img.addClass("rot" + rot * 90)
            }
        }
        return;
    }
    window.specials[key] = 1;
    if (type == 2) {
        var image = "players/" + [
            "hammer_bot",
            "hulk_x90",
            "spin_bot",
            "squash_bot",
            "trundle_bot",
            "twitch",
            "twonky",
            "zoom_bot",
        ][objid];
        var opacity = 1;

    } else if (type == 1) {
        var image = "spawn/" + (objid + 1);
        var opacity = 0.3;
    } else if (type == 0) {
        var image = "flags/" + (objid + 1);
        var opacity = 0.6;
    }
    var img = new Image();
    img.src = "/static/images/" + image + ".png";
    display.append(img);
    $(img).css("z-index", 10 + type);
    $(img).css("opacity", opacity);
    $(img).addClass("rot" + (rot * 90));
    $(img).addClass("floor");
    img.onload = function() {
        img = $(this);
        img.height(squareSize);
        img.width(squareSize);
        squareSize = window.squareSize
        img.css("left", (x * squareSize) + (squareSize - img.width()) / 2);
        img.css("top", (y * squareSize) + (squareSize - img.height()) / 2);
    }
    window.specials[key] = $(img);
}
