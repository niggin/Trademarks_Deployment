RUSSIAN_LANG = 'русский';
ENGLISH_LANG = "англ.";
var colors = ["#d9534f", "#FFCC66", "#6bc873"];
var available_langs = { "en": "Английский", "ru": "Русский", "all": "Все языки" };

$(document).ready(function () {
	loadToggles();
	/*
	 Lang onclick event
	 */
    var word = getUrlAttr("w");
    if (word != "undefined") {
        var lang = getUrlAttr("lt");
        $("#findme").val(word);
        var $choose_language = $("#chooselang");
        var $sort_by = $("#sort-by-button");
        var $transcription = $("#showtranscript");
        if (lang == 'russian' || lang == "undefined") {

        }
        else if (lang == 'english') {
            $choose_language.prop("checked", !$choose_language.prop("checked"));
        }
        var languages = getUrlAttr("groups");
        if (languages) {
            if (languages == ["ru", "en"] || languages == "undefined") {
            } else if (languages == ["all"]) {
                $sort_by.prop("checked", !$sort_by.prop("checked"));
            }
        }
        var trans = true;
        if (getUrlAttr("tr") == "0") {
            trans = false;
            $transcription.prop("checked", !$transcription.prop("checked"));
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
    var search_string = $("#findme").val();
    fetch(search_string, lang.substring(0, 2), true, groups, trans);
    setUrlAttr("w", search_string);
}

function send_report(event)
{
    event.preventDefault();
    if ($("#InputReal").val() == "7")
    {
        $.ajax({
            url: URL_SEND_REPORT,
            type: "POST",
            data: {email: $("#InputEmail").val(), name: $("#InputName").val(),
                message: $("#InputMessage").val(), csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val()},
            success: function (){
                $("#form_ok").show(500);
                $("#form_fail").hide(500);
            }
        });
    }
    else
    {
        $("#form_fail").show(500);
    }
}

function loadListeners() {
    $("#search_button").click(perform_fetch);
    $("#report").submit(send_report);


    $("#main-searcher").submit(perform_fetch);

    $("#showtranscript").click(function () {
        $(".transcript").toggleClass("hidden");
        $(".translate").toggleClass("wide-translate");
        if (typeof getUrlAttr("tr") == "undefined") {
            setUrlAttr("tr", 0);
        } else {
            setUrlAttr("tr", 1 - parseInt(getUrlAttr("tr")));
        }
    });

    $("#sort-by-button").click(function () {
        //sort();
        var languages;
        //var $switcher = $(".onoffswitch-inner.sort-by");
        if ($(this).is(":checked")) {
            languages = ["ru", "en"];
        } else {
            languages = ["all"];
        }
        setUrlAttr("groups", languages);
        var lang = get_currlang();
        var sort = $("#sort-by-button").is(":checked");
        /*if ($("#sort-by-button").is(":checked"))
            sort = false;
        else
            sort = true;*/
        setUrlAttr("lt", lang);
        var trans = true;
        var search_string = $("#findme").val();
        if (getUrlAttr("tr") == 0) trans = false;
        fetch(search_string, lang.substring(0, 2), true, languages, trans);
        setUrlAttr("w", search_string);
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
    $("#resultmode").val(kind);
    var $output = $("#output");
    var $loader = $("#loader");
    if (kind != "") {
        var request = $.ajax({
            url: URL_SEARCH,
            async: async,
            type: "GET",
            data: { findme: kind, translate: lang_out, langs: languages },
            dataType: "json",
            beforeSend: function() {
                $output.css("display", "none");
                $loader.css("display", "");
            },
            success: function(data) {
                for (var lang in data['array']) {
                    var $baselang = $("#lang_template").clone();
                    $baselang.attr("id", "");
                    $baselang.find(".cell.word").html(available_langs[lang]);
                    $baselang.children(".lang_link").attr("id", lang);
                    var $tbody = $baselang.find("tbody");

                    for (var i = 0; i < data['array'][lang].length; i++) {
                        var $word = makeWordEntity(data['array'][lang][i]);
                        $tbody.append($word);
                    }
                    var $loadmore = $("#more").clone();
                    $loadmore.attr("id", "more_" + lang).show();
                    $tbody.append($loadmore);

                    $baselang.show();
                    $output.append($baselang);
                    if (data['hide_morebutton'][lang]) {
                        $("#more_" + lang).css("display", "none");
                    }
                }
                if ($.isEmptyObject(data['array'])) {
                    cleanup();
                    $output.html("<div style='font-size: 14px'>Извините, по Вашему запросу ничего не найдено.</div>");
                } else {
                    getReady();
                }
                if (!trans) {
                    $(".transcript").toggleClass("hidden");
                }
                $loader.css("display", "none");
                $output.css("display", "block");
            }
        });
    }
}

function makeWordEntity(data)
{
    var $word = $("#word_template").clone();
    $word.attr("id","");
    $word.children(".word").html(data[0]['word']);
    $word.children(".transcript").html("[" + data[0]['transcription'] + "]");
    $word.children(".translate").html(data[0]['meaning']);
    var percent = data[1].toFixed(1);
    $word.find(".inner_progressbar").width(percent + "%").css("background-color", colors[parseInt(percent / 34)]);

    $word.show();
    return $word;
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
        fetch_more($(this).attr('id').substring(5), $("#resultmode").val());
    });

    $(".lang-header .word").click(function () {
        $(this).parent().focuseOn();
    });
}

function fetch_more(lang_out, word) {
    var request = $.ajax({
        url: URL_LOAD_MORE,
        type: "GET",
        data: { lang: lang_out, findme: word },
        dataType: "json",
        async: false,
        success: function (data) {
            var trans = getUrlAttr("tr") == "0";
            for (var lang in data['array']) {
                for (var i = 0; i < data['array'][lang].length; i++) {
                    var $word = makeWordEntity(data['array'][lang][i]);
                    $word.insertBefore("#more_" + lang);
                }
                var $lang = $("#more_" + lang);
                if (data['hide_morebutton'][lang]) {
                    $lang.css("display", "none");
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
    //console.log(typeof (q[key]) + " " + q[key] + " " + key);
    return answer;
}

function send_user_reaction(positive)
{
    var input_word = $("#resultmode").val();
    var to_word = $(this).parent().parent().find(".word").html();
    var $glyphs = $(this).parent().parent().find(".glyphicon");
    $.ajax({
        url: URL_SEND_USER_REACTION,
        data: {input_word: input_word, like: positive, to_word: to_word, csrfmiddlewaretoken: CSRF_TOKEN.val()},
        type: "POST",
        success: function (){
            $glyphs.each(function()
            {
                $(this).hide();
            });
        }
    });
}