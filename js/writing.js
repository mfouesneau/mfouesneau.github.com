function name_to_abbrev(name) {
    // Given a full name, return just initials until last name
    var names = name.split(" ");
    var lastName = names.slice(-1)[0];

    var returnName = "";
    for (var i=0; i < (names.length-1); i++) {
        returnName += names[i][0] + ". ";
    }
    return returnName + lastName
}

// Load recent paper list
function setupWriting() {
    var n = 3; // number of papers

    $.ajax({
        url: 'http://export.arxiv.org/api/query?search_query=au:price_whelan+cat:astro-ph&start=0&max_results=100&sortBy=submittedDate', // or lastUpdatedDate
        type: 'GET',
        dataType: "xml",
        async: true,
        success: function(xml) {
            $("#recent-papers").empty();
            var num = 0;
            $(xml).find("entry").each(function(){
                var title = $(this).find("title").text().replace(/(\r\n|\n|\r)/gm,""),
                    link = $(this).find("id").text(),
                    rawDate = $(this).find("published").text(),
                    firstAuthor = $(this).find("author").find("name").first().text();

                // Author stuff
                var lastName = firstAuthor.split(" ").slice(-1)[0];
                if (lastName.toLowerCase() != "price-whelan") {
                    return;
                }

                var authors = $(this).find("author").find("name"),
                    strAuthor;
                if (authors.length == 1) {
                    strAuthor = name_to_abbrev(authors.first().text());
                } else if (authors.length == 2) {
                    strAuthor = name_to_abbrev(authors.first().text()) + " & " + name_to_abbrev(authors.last().text());
                } else {
                    strAuthor = "";
                    for (var i=0; i < authors.length; i++) {
                        if (i == 0)
                            strAuthor = name_to_abbrev($(authors[i]).text());
                        else
                            strAuthor += ", " + name_to_abbrev($(authors[i]).text());
                        if (i >= 4) break;
                    }
                    // add et al. to end because there are more authors
                    if (i != authors.length)
                        strAuthor = strAuthor + " et al.";

                }

                var authorSpan = $('<span>');
                authorSpan.addClass("author");
                authorSpan.text(strAuthor);

                // Date stuff
                var date = rawDate.split("T")[0].split("-");
                var dateSpan = $('<span>');
                dateSpan.addClass('date');
                dateSpan.text("(" + date[1] + "/" + date[0] + ")");

                // Main paragraph element
                var p = $('<p>');
                p.css("opacity", 0.);

                var a = $('<a>');
                a.attr("href", link);
                a.text(title);

                p.append(dateSpan);
                p.append(authorSpan);
                p.append("<br/>")
                p.append(a);
                $("#recent-papers").append(p);
                num = num + 1;

                p.animate({ opacity: 1}, 1000);

                if (num >= n) {
                    return false;
                }
            });
        },
        error: function (XMLHttpRequest, textStatus, errorThrown) {
            var p = $('<p>');
            p.html("Unable to retrieve paper list!");
            p.addClass("error");
            $("#recent-papers").append(p);
        }
    });
}