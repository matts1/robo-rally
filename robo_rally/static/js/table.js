document.ready = function () {
    tables = $(".magictable")
    for (var i = 0; i < tables.length; i++) {
        setupTable(tables[i]);
    }
}

function setupTable (table) {
    thead = $("thead", table);
    needFilterRow = false;
    filterRow = $("<tr></tr>");
    row = $("tr th", thead);
    for (var i = 0; i < row.length; i++) {
        filter = $(row[i]).attr("data-filter");
        col = $("<th></th>")
        if (filter != undefined) {
            needFilterRow = true;
        }
        if (filter == "text") {
            col.append("<input>");
            col.on('keyup', 'input', textFilter);
        } else if (filter == "select") {
            col.append("<select><option value=''>All</option></select>");
            rows = $("tbody tr", table);
            vals = {};
            for (var j = 0; j < rows.length; j++) {
                vals[$($(rows[j]).children()[i]).text()] = true;
            }
            select = $("select", col);
            for (var key in vals) {
                select.append("<option>" + key + "</option>")
            }
            col.on("change", "select", textFilter);
        }
        filterRow.append(col);
    }
    if (needFilterRow) {
        thead.append(filterRow);
    }
}

function textFilter () {
    regex = new RegExp("\\b" + $(this).val(), 'i');
    item = $(this).parent();
    index = item.parent().children().index(item);
    rows = $("tbody tr", item.parent().parent().parent());
    for (var i = 0; i < rows.length; i++) {
        square = $($(rows[i]).children()[index]);
        if (square.text().match(regex)) {
            square.removeClass("nomatch");
        } else {
            square.addClass("nomatch");
        }
    };
    changeDisplay(rows);
}

function changeDisplay (rows) {
    for (var i = 0; i < rows.length; i++) {
        row = $(rows[i]);
        remove = $("td.nomatch", row).length > 0;
        removed = row.hasClass("nomatchrow");
        if (remove && !removed) {
            row.addClass("nomatchrow");
            row.slideUp();
        } else if (removed && !remove) {
            row.removeClass("nomatchrow");
            row.slideDown();
        }
    }
}
