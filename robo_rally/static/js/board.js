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

function loadBoard(obj, url) {
    obj = $(obj);
    obj.toggleClass("rot180");
    tr = obj.parent().parent();
    if ($(".boarddisplay", tr).length) {
        $(".boarddisplay", tr).parent().toggleClass("invisible");
        return;
    }
    overlay = $("<td class='newline'><div class='boarddisplay'></div></td>");
    $(obj).parent().parent().append(overlay);
    $.get(url, {}, function(data) {
        data = $(data);
        var fields = [
            "name", "description", "rules", "length", "difficulty",
            "minplayers", "maxplayers", "numflags"
        ];
        for (var i = 0; i < fields.length; i++) {
            var field = fields[i];
            overlay.append("<div class='" + field + "'></div>");
            $($("." + field)[0]).html($("." + field, data).html());
        }
        window.specials = {};
        drawBoard($(".boarddisplay", overlay), $(".board", data), $(".spawn", data), $(".flags", data));
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
            img.src = "/static/images/" + FILES[parseInt(square[0])];
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
                img.src = "/static/images/" + FILES[parseInt(square[i + 2])];
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
            drawSpecial(0, i, parseInt(coords[0]), parseInt(coords[1]), 0);
        }
    }
    for (var i = 0; i < spawn.length; i++) {
        coords = spawn[i].split(",");
        drawSpecial(1, i, parseInt(coords[0]), parseInt(coords[1]), 0);
        drawSpecial(2, i, parseInt(coords[0]), parseInt(coords[1]), 1);
    }
};

function drawSpecial(type, objid, x, y, rot) {
    key = (8 * type) + objid;
    if (key in window.specials) {
        window.specials[key].remove()
    }
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
    $("#boarddisplay").append(img);
    $(img).css("z-index", 10 + type);
    $(img).css("opacity", opacity);
    $(img).addClass("rot" + (rot * 90));
    $(img).addClass("floor");
    img.onload = function() {
        img = $(this);
        var height = parseInt(img.css("height"));
        var width = parseInt(img.css("width"));
        squareSize = window.squareSize
        img.css("left", (x * squareSize) + (squareSize - width) / 2);
        img.css("top", (y * squareSize) + (squareSize - height) / 2);
    }
    window.specials[key] = $(img);
}
