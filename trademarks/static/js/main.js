$(document).ready(function () {
	loadToggles();
	/*
	 Lang onclick event
	 */
    var word = getUrlAttr("w");
    console.log(word);
    if (word != "undefined") {
        console.log("ready run");
        var lang = getUrlAttr("lt");
        $("#findme").val(word);
        if (lang == "russian" || lang == "undefined") {
            
        }
        else if (lang == "english") {
            $("#chooselang").prop("checked", !$("#chooselang").prop("checked"));
        }
        console.log(languages, "ready");
        var languages = getUrlAttr("groups");
        if (languages) {
            if (languages == ["ru", "en"] || languages == "undefined") {
            } else if (languages == ["all"]) {
                $("#sort-by-button").prop("checked", !$("#sort-by-button").prop("checked"));
            }
        }
        var trans = true;
        if (getUrlAttr("tr") == "0") {
            trans = false;
            $("#showtranscript").prop("checked", !$("#showtranscript").prop("checked"));
        }
        fetch(word, lang.substring(0, 2), false, languages, trans);
        
        //$("#output").css("display", "");
    }
    loadListeners();
});

function loadToggles() {
    $.fn.focuseOn = function(){
        if(!$(this).parent(".lang").hasClass("focused")) {
            var $focusedobject = $(this);
            var $opaco = $("<div/>", {
                id: "opaco",
            });
            $("body").append($opaco);
            $($opaco).height($(document).height())
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
        $(this).parent(".lang").toggleClass('focused');
        $(this).toggleClass("focused");
    }

}

function loadListeners() {
    $("#search_button").click(function () {
        var lang = get_currlang();
        var groups = getUrlAttr("groups");
        setUrlAttr("lt", lang);
        var trans = true;
        if (getUrlAttr("tr") == 0) trans = false;
        fetch($("#findme").val(), lang.substring(0, 2), true, groups, trans);
        setUrlAttr("w", $("#findme").val());
    });

    $("#findme").keyup(function (event) {
        if (event.keyCode == 13) {
            $("#search_button").click();
        }
    });

    $("#showtranscript").click(function () {
        $(".transcript").toggleClass("hidden");
        $(".translate").toggleClass("wide-translate");
        if (getUrlAttr("tr") == "undefined") {
            setUrlAttr("tr", 0);
        } else {
            setUrlAttr("tr", 1 - getUrlAttr("tr"));
        }
    });

    $("#sort-by-button").click(function () {
        //sort();
        var languages;
        var $switcher = $(".onoffswitch-inner.sort-by");
        if ($(this).is(":checked")) {
            languages = ["ru", "en"];
        } else {
            languages = ["all"];
        }
        setUrlAttr("groups", languages);
        var lang = get_currlang();
        var sort;
        if ($("#sort-by-button").is(":checked"))
            sort = false;
        else
            sort = true;
        setUrlAttr("lt", lang);
        var trans = true;
        if (getUrlAttr("tr") == 0) trans = false;
        fetch($("#findme").val(), lang.substring(0, 2), true, languages, trans);
        setUrlAttr("w", $("#findme").val());
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
        $("#search_button").click();
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
    value = String(value).replace(/"/g, '');
    console.log(value, "set");
    q[key] = value;
    history.pushState('', 'xz', '?' + queryString.stringify(q));
}

function fetch(kind, lang_out, async, languages, trans) {
    async = async != 'undefined' ? async : true;
    trans = trans != 'undefined' ? trans : true;
    languages = languages != 'undefined' ? languages : ["ru", "en"];
    if (typeof (languages) == "string") languages = [languages];
    console.log(async, trans, languages, lang_out);
    cleanup();
    available_langs = { "en": "English", "ru": "Russian", "all": "All languages" };
    var request = $.ajax({
        url: "/search",
        async: async,
        type: "GET",
        data: { findme: kind, translate: lang_out, langs: languages },
        dataType: "json",
        beforeSend: function () {
            $("#output").css("display", "none");
            $("#loader").css("display", "");
        },
        success: function (data) {
            var colors = ["#ff0000", "#ffd700", "#00ff00"];
            for (var lang in data['array']) {
               
                var $baselang = $("<div/>", { class: "lang" });
                $baselang.append("<div class='wordline lang-header'><div class='cell word'>" + available_langs[lang] + "</div>");
                var $lang = $("<div/>", { class: "lang_link", id: lang }).appendTo($baselang);

                for (var i = 0; i < data['array'][lang].length; i++) {
                    var $word = $("<div/>", { class: "wordline" });
                    var $input = $("<div/>", { class: "cell word" }).html(data['array'][lang][i][0]['word']).appendTo($word);
                    $input = $("<div/>", { class: "cell transcript" }).html("[" + data['array'][lang][i][0]['transcription'] + "]").appendTo($word);
                    $input = $("<div/>", { class: "cell translate" }).html(data['array'][lang][i][0]['meaning']).appendTo($word);
                    var percent = data['array'][lang][i][1].toFixed(1);
                    $input = $("<div/>", { class: "cell percent" });
                    var $progress = $("<div/>", { class: "progressbar" }).appendTo($input);
                    var $ch = $("<div/>", { width: percent + "%" }).css("background-color", colors[parseInt(percent / 34)]).appendTo($progress);
                    $input.appendTo($word);
                    $baselang.append($word);
                }
                $baselang.append($("<div/>", { class: "loadmore", id: "more_" + lang }).html("show more results"));
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

            console.log(trans, "fetch");
            if (!trans) {
                $(".transcript").toggleClass("hidden");
            }
            $("#loader").css("display", "none");
            $("#output").css("display", "block");
        }
    });
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

    $(".loadmore").click(function () {
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
        async: false,
        success: function (data) {
            var trans = getUrlAttr("tr") == "0";
            var colors = ["#ff0000", "#ffd700", "#00ff00"];
            for (var lang in data['array']) {
                var $baselang = $("#" + lang).parent();
                for (var i = 0; i < data['array'][lang].length; i++) {
                    var $word = $("<div/>", { class: "wordline" });
                    var $input = $("<div/>", { class: "cell word" }).html(data['array'][lang][i][0]['word']).appendTo($word);
                    $input = $("<div/>", { class: "cell transcript" }).html("[" + data['array'][lang][i][0]['transcription'] + "]").appendTo($word);
                    $input = $("<div/>", { class: "cell translate" }).html(data['array'][lang][i][0]['meaning']).appendTo($word);
                    var percent = data['array'][lang][i][1].toFixed(1);
                    $input = $("<div/>", { class: "cell percent" });
                    var $progress = $("<div/>", { class: "progressbar" }).appendTo($input);
                    var $ch = $("<div/>", { width: percent + "%" }).css("background-color", colors[parseInt(percent / 34)]).appendTo($progress);
                    $input.appendTo($word);
                    $baselang.append($word);
                }
                $("#more_" + lang).appendTo($baselang);
                if (data['hide_morebutton'][lang]) {
                    $("#more_" + lang).css("display", "none");
                }
                //console.log($baselang.children());
            }
            if (trans) {
                    $(".transcript").toggleClass("hidden", true);
                }
        }
    });
}

function get_currlang() {
    var $switcher = $(".onoffswitch-inner.chooselang");
    var lang = String();
    if ($("#chooselang").is(":checked"))
        $switcher.each(function () {
            lang = window.getComputedStyle(this, ':before').content;
        });
    else
        $switcher.each(function () {
            lang = window.getComputedStyle(this, ':after').content;
        });
    console.log(lang.replace(/"/g, ''), "get_currlang");
    return lang.replace(/"/g,'');
}

function getUrlAttr(key) {
    var q = queryString.parse(location.search);
    console.log(q[key], "get", key);
    return String(q[key]).replace(/"/g, '');
}
