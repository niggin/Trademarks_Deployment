RUSSIAN_LANG = 'русский';
ENGLISH_LANG = "англ.";

$(document).ready(function () {
	loadToggles();
	/*
	 Lang onclick event
	 */
    var word = getUrlAttr("w");
    if (word != "undefined") {
        var lang = getUrlAttr("lt");
        $("#findme").val(word);
        if (lang == 'russian' || lang == "undefined") {

        }
        else if (lang == 'english') {
            $("#chooselang").prop("checked", !$("#chooselang").prop("checked"));
        }
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
        //lang = lang.replace("\"","").replace("'","");
        if (typeof (word) != "undefined") {
            fetch(word, lang.substring(0, 2), false, languages, trans);
        }
        
        //$("#output").css("display", "");
    }
    loadListeners();
});

function loadToggles() {
    $.fn.focuseOn = function(){
        if(!$(this).parent(".lang").hasClass("focused")) {
            var $focusedobject = $(this);
            var $opaco = $("<div/>", {
                id: "opaco"
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

function perform_fetch(event) {
    event.preventDefault();
    var lang = get_currlang();
    var groups = getUrlAttr("groups");
    setUrlAttr("lt", lang);
    var trans = true;
    if (getUrlAttr("tr") == 0) trans = false;
    fetch($("#findme").val(), lang.substring(0, 2), true, groups, trans);
    setUrlAttr("w", $("#findme").val());
}

function loadListeners() {
    $("#search_button").click(perform_fetch);

    $("#main-searcher").submit(perform_fetch);

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

    // var searchTop = $("#header-background").offset().top;
    // $(window).scroll(function(){ 
    //     var scrollTop = $(window).scrollTop();
    //     if(scrollTop > searchTop) {
    //         $("#header-background").css("position", "fixed");
    //     } else {
    //         $("#header-background").css("position", "relative"); 
    //     }
    // });

}

function setUrlAttr(key, value) {
    var q = queryString.parse(location.search);
    if(typeof (value) == "string") value = String(value).replace(/"/g, '');
    q[key] = value;
    history.pushState('', 'xz', '?' + queryString.stringify(q));
}

function fetch(kind, lang_out, async, languages, trans) {
    async = typeof async != 'undefined' ? async : true;
    trans = typeof trans != 'undefined' ? trans : true;
    languages = typeof languages != 'undefined' ? languages : ["ru", "en"];
    if (typeof (languages) == "string") languages = [languages];
    cleanup();
    var available_langs = { "en": "Английский", "ru": "Русский", "all": "Все языки" };
    if (kind != "") {
        var request = $.ajax({
            url: "/search",
            async: async,
            type: "GET",
            data: { findme: kind, translate: lang_out, langs: languages },
            dataType: "json",
            beforeSend: function() {
                $("#output").css("display", "none");
                $("#loader").css("display", "");
            },
            success: function(data) {
                var colors = ["#d9534f", "#FFCC66", "#6bc873"];
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
                    $baselang.append($("<div/>", { class: "loadmore", id: "more_" + lang }).html("загрузить больше результатов"));
                    $("#output").append($baselang);
                    if (data['hide_morebutton'][lang]) {
                        $("#more_" + lang).css("display", "none");
                    }
                }
                if ($.isEmptyObject(data['array'])) {
                    cleanup();
                    $("#output").html("<div style='font-size: 14px'>Извините, по Вашему запросу ничего не найдено.</div>");
                } else {
                    getReady();
                }
                if (!trans) {
                    $(".transcript").toggleClass("hidden");
                }
                $("#loader").css("display", "none");
                $("#output").css("display", "block");
            }
        });
    }
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
            var colors = ["#d9534f", "#FFCC66", "#6bc873"];
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
            lang = 'russian'; // window.getComputedStyle(this, ':before').content;
        });
    else
        $switcher.each(function () {
            lang = 'english'; // window.getComputedStyle(this, ':after').content;
        });
    return lang.replace(/"/g,'');
}

function getUrlAttr(key) {
    var q = queryString.parse(location.search);
    var answer;
    if (typeof (q[key]) == "string") {
        answer = String(q[key]).replace(/"/g, '');
    } else {
        answer = q[key];
    }
    console.log(typeof (q[key]) + " " + q[key] + " " + key);
    return answer;
}
