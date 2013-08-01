function to2d (whole) {
    rows = whole.children();
    for (var y = 0; y < rows.length; y++) {
        rows[y] = $(rows[y]).children();
        for (var x = 0; x < rows[y].length; x++) {
            rows[y][x] = $(rows[y][x]);
        }
    }
    return rows;
}

document.ready = function () {
    if ($("table#magictable") == undefined) {
        console.log("no magictable");
        return;
    }
    window.thead = to2d($("table#magictable thead"));
    window.tbody = to2d($("table#magictable tbody"));
    needFilterRow = false;
    filterRow = $("<tr></tr>");
    cols = window.thead[0];
    for (var i = 0; i < cols.length; i++) {
        filter = $(cols[i]).attr("data-filter");
        col = $("<th></th>")
        if (filter != undefined) {
            needFilterRow = true;
        }
        if (filter == "text") {
            col.append("<input>");
            col.on('keyup', 'input', {method: "startword", index: i}, textFilter);
        } else if (filter == "select") {
            col.append("<select><option value=''>All</option></select>");
            select = $("select", col);
            options = cols[i].attr("data-options").split("|");
            for (var j = 0; j < options.length; j++) {
                select.append("<option>" + options[j] + "</option>")
            }
            col.on("change", "select", {method: "exact", index: i}, textFilter);
        }
        filterRow.append(col);
    }
    if (needFilterRow) {
        $("table#magictable thead").append(filterRow);
    }
}

function textFilter (event) {
    val = $(this).val().replace(/[\-\[\]\/\{\}\(\)\*\+\?\.\\\^\$\|]/g, "\\$&"); // escaped
    if (val == "") {
        val = undefined;
    }
    regexstart = new RegExp("\\b" + val, 'i');
    index = event.data.index;
    method = event.data.method;
    for (var y = 0; y < window.tbody.length; y++) {
        square = window.tbody[y][index];
        if (method == "exact") {
            valid = (square.text() == val) || (val == undefined);
        } else if (method == "startword") {
            valid = (val == undefined) || square.text().match(regexstart);
        }
        row = $(square.parent());
        expanded = $("td:last-child img.button.rot180", row).length > 0;
        if (valid) {
            square.removeClass("nomatch");
            for (var x = 0; x < window.tbody[y].length; x++) {
                if (window.tbody[y][x].hasClass("nomatch")) {
                    valid = false;
                    break;
                }
            }
            if (valid) {
                row.slideDown();
            }
        } else {
            if (expanded) {
                row.next().addClass("invisible");
                $("td:last-child img.button.rot180", row).removeClass("rot180");
            }
            square.addClass("nomatch");
            row.slideUp();
        }
    }
}
