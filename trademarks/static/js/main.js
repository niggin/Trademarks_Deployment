$(document).ready(function () {
	loadToggles();
	/*
	 Lang onclick event
	 */
    
    loadListeners();
});

$("document").ready(function (event, data) {
    var word = getUrlAttr("w");
    var $switcher = $(".onoffswitch-inner.chooselang");
    if (word) {
        var lang = getUrlAttr("lt");
        $("#findme").val(word);
        if (lang == "english")
            $switcher.each(function () {
                lang = window.getComputedStyle(this, ':before').content;
            });
        else if (lang == "russian") {
            $switcher.each(function() {
                lang = window.getComputedStyle(this, ':after').content;
            });
            $("#chooselang").prop("checked", !$("#chooselang").prop("checked"));
        }
        var languages = getUrlAttr("lf");
        fetch(word, lang.substring(0, 2), false, languages);
        if (typeof getUrlAttr("tr") != "undefined") $("#showtranscript").click();
        var sorting = getUrlAttr("sort");
        if (sorting) {
            $switcher = $(".onoffswitch-inner.sort-by");
            if (sorting == "language")
                $switcher.each(function() {
                    setUrlAttr("sort", window.getComputedStyle(this, ':before').content);
                });
            else {
                $switcher.each(function() {
                    setUrlAttr("sort", window.getComputedStyle(this, ':after').content);    
                });
                $("#sort-by-button").prop("checked", !$("#sort-by-button").prop("checked"));
                sort();
            }
        }
        //$("#output").css("display", "");
    }
});

function loadToggles() {
    $.fn.focuseOn = function () {
        if(!$(this).parent(".lang").hasClass("focused")) {
        	$focusedobject = $(this);
        	$opaco = $("<div/>", {
        		id: "opaco"
        	});
        	$("body").append($opaco);
            $($opaco).height($(document).height())
            		.toggleClass('hidden')
            		.fadeTo('fast', 0.7)
            		.click(function(){
            			$focusedobject.focuseOff();
            		});
            $focusedobject.parent(".lang").toggleClass("focused");
            $focusedobject.toggleClass("focused");
        } else  {
        	$(this).focuseOff();
        }
    };
    $.fn.focuseOff = function() {
        $("#opaco").remove();
        $("#opaco").toggleClass('hidden').removeAttr('style').unbind('click');
        $(this).parent(".lang").toggleClass('focused');
        $(this).toggleClass("focused");
    };

}

function loadListeners() {
    $("#search_button").click(function () {
        var lang = get_currlang();
        setUrlAttr("lt", lang);
        fetch($("#findme").val(), lang.substring(0,2));
        setUrlAttr("w", $("#findme").val());
    });

    $("#findme").keyup(function (event) {
        if (event.keyCode == 13) {
            $("#search_button").click();
        }
    });

    $("#showtranscript").click(function () {
        $(".transcript").toggleClass("hidden");

    });

    $("#sort-by-button").click(function () {
        sort();
        var $switcher = $(".onoffswitch-inner.sort-by");
        if($(this).is(":checked"))
            $switcher.each(function() {
                setUrlAttr("sort", window.getComputedStyle(this,':before').content);
            });
        else
            $switcher.each(function() {
                setUrlAttr("sort", window.getComputedStyle(this,':after').content);
            });
    });

    $(".lang_link").click(function () {
        $(this).focuseOn();
        
    });

    $(".more").click(function () {
        $(this).parent().focuseOn();
    });

    $(".lang-header .word").click(function () {
        $(this).parent().focuseOn();
    });

    $("#chooselang").click(function () {
        var lang = get_currlang();
        setUrlAttr("lt", lang);
        fetch($("#findme").val(), lang.substring(0,2));
    });

    var searchTop = $("#header-background").offset().top;
    $(window).scroll(function(){ 
        var scrollTop = $(window).scrollTop();
        if(scrollTop > searchTop) {
            $("#header-background").css("position", "fixed");
        } else {
            $("#header-background").css("position", "relative"); 
        }
    });

}

function setUrlAttr(key, value) {
    var q = queryString.parse(location.search);
    console.log(q);
    q[key] = value;
    history.pushState('', 'xz', '?' + queryString.stringify(q));
}

function sort() {
    $(".percent_button").toggleClass('active');
    $.ajax({
        beforeSend: function() {
            $("#output").css("display", "none");
            $("#loader").css("display", "");
        },
        success: function () {
            sortByMatch(get_currlang().substring(0,2));
            //sortByMatch();
            $("#loader").css("display", "none");
            $("#output").css("display", "block");
        }
    });
}

function fetch(kind, lang_out, async, languages) {
    async = typeof (async) != 'undefined' ? async : true;
    languages = typeof (languages) != 'undefined' ? languages : ["ru", "en", "ge"];
    if (typeof (languages) == "string") languages = [languages];
    cleanup();
    var request = $.ajax({
        url: "/search",
        async: async,
        type: "GET",
        data: { findme: kind, translate: lang_out, langs: languages },//getAttrFromUrl("lt"), langs: getAttrFromUrl("lf"), sort: getAttrFromUrl("sort") },
        dataType: "json",
        beforeSend: function() { 
            $("#output").css("display", "none");
            $("#loader").css("display", "");
        },
        success: function (data) {
            for (var lang in data['array']) {
               
                var $baselang = $("<div/>", { class: "lang" });
                $baselang.append("<div class='wordline lang-header'><div class='cell word'>" + lang + "</div><div class='more' id='" + "more_" + lang + "'>more</div></div>");
                var $lang = $("<div/>", { class: "lang_link", id: lang }).appendTo($baselang);

                for (var i = 0; i < data['array'][lang].length; i++) {
                    var $word = $("<div/>", { class: "wordline" });
                    var $input = $("<div/>", { class: "cell word" }).html(data['array'][lang][i][0]['word']).appendTo($word);
                    $input = $("<div/>", { class: "cell transcript" }).html("[" + data['array'][lang][i][0]['transcription'] + "]").appendTo($word);
                    $input = $("<div/>", { class: "cell translate" }).html(data['array'][lang][i][0]['meaning']).appendTo($word);
                    $input = $("<div/>", { class: "cell percent" }).html(data['array'][lang][i][1].toFixed(1) + "%").appendTo($word);
                    $baselang.append($word);
                }
                $("#output").append($baselang);
                if (data['hide_morebutton'][lang]) {
                    $("#more_" + lang).css("display", "none");
                }
            }
            if ($.isEmptyObject(data['array'])) {
                cleanup();
            } else {
                getReady();
            }
            $("#loader").css("display", "none");
            $("#output").css("display", "block");
        }
    });
}


function sortByMatch(lang_skip) {
    var $source = $("#output");
    var $tohide = $("#tohide");

    if ($tohide.html().localeCompare("")) {
        $source.html($tohide.html());
        $tohide.html("");
    } else {
        var langs = $.makeArray($source.children());
        var allwords = new Array();

        for (var item in langs) {
            var temparray = $.makeArray(langs[item].children);
            temparray.splice(0, 1);
            for (var i = 1; i < temparray.length; i++) {
                if (temparray[0].id == lang_skip) {
                    var toarray = temparray[i].cloneNode(true);
                    toarray.children[2].innerHTML = temparray[i].children[0].innerHTML;
                    allwords.push(toarray);
                } else {
                    allwords.push(temparray[i]);
                }
            }
        }

        allwords.sort(function (a, b) {
            var aord = a.children[3].innerHTML;
            var bord = b.children[3].innerHTML;
            return parseInt(bord) - parseInt(aord);
        });

        $tohide.html($source.html());
        $source.html("");

        var $baselang = $("<div/>", {
            class: "lang",
            id: "baselang"
        });

        var $lang = $("<div/>", {
            class: "lang_link",
            id: "all"
        }).appendTo($baselang);

        $baselang.append("<div class='wordline lang-header'><div class='cell word'>All languages</div>");

        for (i = 0; i < allwords.length; i++) {
            $baselang.append(allwords[i]);
        }

        $source.append($baselang);
    }

    getReady();
    
}

function cleanup() {
    $("#loader").css("display", "none");
    if ($("#tohide").html().localeCompare("")) {
        $("#tohide").html("");
        $(".percent_button").toggleClass('active');
    }
    $("#output").html("");
}

function getReady() {
    $(".lang_link").click(function () {
        $(this).focuseOn();
    });

    $(".more").click(function () {
        fetch_more($(this).attr('id').substring(5));
    });

    $(".lang-header .word").click(function () {
        $(this).parent().focuseOn();
    });
}

function fetch_more(lang_out) {
    var request = $.ajax({
        url: "/load_more",
        type: "GET",
        data: { lang: lang_out },
        dataType: "json",
        success: function(data) {
            for (var lang in data['array']) {
                var $baselang = $("#" + lang).parent();
                for (var i = 0; i < data['array'][lang].length; i++) {
                    var $word = $("<div/>", { class: "wordline" });
                    var $input = $("<div/>", { class: "cell word" }).html(data['array'][lang][i][0]['word']).appendTo($word);
                    $input = $("<div/>", { class: "cell transcript" }).html("[" + data['array'][lang][i][0]['transcription'] + "]").appendTo($word);
                    $input = $("<div/>", { class: "cell translate" }).html(data['array'][lang][i][0]['meaning']).appendTo($word);
                    $input = $("<div/>", { class: "cell percent" }).html(data['array'][lang][i][1].toFixed(1) + "%").appendTo($word);
                    $baselang.append($word);
                    if (data['hide_morebutton'][lang]) {
                        $("#more_" + lang).css("display", "none");
                    }
                }
            }
        }
    });
}

function get_currlang() {
    var $switcher = $(".onoffswitch-inner.chooselang");
    var lang;
    if ($("#chooselang").is(":checked"))
        $switcher.each(function () {
            lang = window.getComputedStyle(this, ':before').content;
        });
    else
        $switcher.each(function () {
            lang = window.getComputedStyle(this, ':after').content;
        });
    return lang;
}

function getUrlAttr(key) {
    var q = queryString.parse(location.search);
    return q[key];
}
