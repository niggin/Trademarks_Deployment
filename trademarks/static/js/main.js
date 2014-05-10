$(document).ready(function () {
	loadToggles();
	/*
	 Lang onclick event
	 */
    
    loadListeners();
});

$("document").ready(function (event, data) {
    var word = getUrlAttr("w");
    console.log(word);
    if (word != "undefined") {
        console.log("ready run");
        var lang = getUrlAttr("lt");
        $("#findme").val(word);
        if (lang == "english" || lang == "undefined") {
            
        }
        else if (lang == "russian") {
            $("#chooselang").prop("checked", !$("#chooselang").prop("checked"));
        }
        var languages = getUrlAttr("lf");
        console.log(languages, "ready");
        var sorting = getUrlAttr("sort");
        var sort_li;
        if (sorting) {
            if (sorting == "percents" || sorting == "undefined") {
                sort_li = false;
            } else if (sorting == "similarity") {
                $("#sort-by-button").prop("checked", !$("#sort-by-button").prop("checked"));
                sort_li = true;
            }
        }
        var trans = true;
        if (getUrlAttr("tr") == "0") {
            trans = false;
            $("#showtranscript").prop("checked", !$("#showtranscript").prop("checked"));
        }
        fetch(word, lang.substring(0, 2), false, languages, sort_li, trans);
        
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
        var sort;
        if ($("#sort-by-button").is(":checked"))
            sort = false;
        else
            sort = true;
        setUrlAttr("lt", lang);
        var trans = true;
        if (getUrlAttr("tr") == 0) trans = false;
        fetch($("#findme").val(), lang.substring(0, 2), true, ["ru", "en"], sort, trans);
        setUrlAttr("w", $("#findme").val());
    });

    $("#findme").keyup(function (event) {
        if (event.keyCode == 13) {
            $("#search_button").click();
        }
    });

    $("#showtranscript").click(function () {
        $(".transcript").toggleClass("hidden");
        if (getUrlAttr("tr") == "undefined") {
            setUrlAttr("tr", 0);
        } else {
            setUrlAttr("tr", 1 - getUrlAttr("tr"));
        }
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

function sort() {
    //$(".percent_button").toggleClass('active');
    sortByMatch(get_currlang().substring(0, 2));
}

function fetch(kind, lang_out, async, languages, sort, trans) {
    async = async != 'undefined' ? async : true;
    trans = trans != 'undefined' ? trans : true;
    sort = sort != 'undefined' ? sort : false;
    languages = languages != 'undefined' ? languages : ["ru", "en"];
    if (typeof (languages) == "string") languages = [languages];
    console.log(async, trans, sort, languages, lang_out);
    cleanup();
    var request = $.ajax({
        url: "/search",
        async: async,
        type: "GET",
        data: { findme: kind, translate: lang_out, langs: languages },//getAttrFromUrl("lt"), langs: getAttrFromUrl("lf"), sort: getAttrFromUrl("sort") },
        dataType: "json",
        beforeSend: function () {
            $("#output").css("display", "none");
            $("#loader").css("display", "");
        },
        success: function (data) {
            var colors = ["#ff0000", "#ffd700", "#00ff00"];
            for (var lang in data['array']) {
               
                var $baselang = $("<div/>", { class: "lang" });
                $baselang.append("<div class='wordline lang-header'><div class='cell word'>" + lang + "</div>");//"<div class='more' id='" + "more_" + lang + "'>more</div></div>");
                var $lang = $("<div/>", { class: "lang_link", id: lang }).appendTo($baselang);

                for (var i = 0; i < data['array'][lang].length; i++) {
                    var $word = $("<div/>", { class: "wordline" });
                    var $input = $("<div/>", { class: "cell word" }).html(data['array'][lang][i][0]['word']).appendTo($word);
                    $input = $("<div/>", { class: "cell transcript" }).html("[" + data['array'][lang][i][0]['transcription'] + "]").appendTo($word);
                    $input = $("<div/>", { class: "cell translate" }).html(data['array'][lang][i][0]['meaning']).appendTo($word);
                    //$input = $("<div/>", { class: "cell percent" }).html(data['array'][lang][i][1].toFixed(1) + "%").appendTo($word);
                    var percent = data['array'][lang][i][1].toFixed(1);
                    $input = $("<div/>", { class: "progressbar" });
                    var $ch = $("<div/>", { width: percent }).css("background-color", colors[parseInt(percent/34)]).appendTo($input);
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
            if (sort) {
                sortByMatch(lang_out);
            }
            console.log(trans, "fetch");
            if (!trans) {
                $(".transcript").toggleClass("hidden");
            }
            $("#loader").css("display", "none");
            if (!sort) $("#output").css("display", "block");
        }
    });
}


function sortByMatch(lang_skip) {
    var $source = $("#output");
    var $tohide = $("#tohide");

    if ($tohide.html().localeCompare("")) {
        //$source.html($tohide.html());
        $source.css("display", "block");
        $tohide.html("");
    } else {
        var langs = $.makeArray($source.children());
        var allwords = new Array();

        for (var item in langs) {
            var temparray = $.makeArray(langs[item].children);
            temparray.splice(0, 1);
            for (var i = 1; i < temparray.length - 1; i++) {
                if (temparray[0].id == lang_skip) {
                    //temparray[i].id = i;
                    //alert(temparray[i].children[0].innerHTML);
                    var toarray = temparray[i].cloneNode(true);
                    toarray.children[2].innerHTML = temparray[i].children[0].innerHTML;
                    allwords.push(toarray);
                } else {
                    allwords.push(temparray[i].cloneNode(true));
                }
            }
        }
        
        allwords.sort(function (a, b) {
            var aord = a.children[3].innerHTML;
            var bord = b.children[3].innerHTML;
            return parseFloat(bord) - parseFloat(aord);
        });

        //$tohide.html($source.html());
        //$source.html("");

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

        //$source.append($baselang);
        $tohide.append($baselang);
        $tohide.css("display", "block");
        $source.css("display", "none");
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
        success: function (data) {
            var trans = getUrlAttr("tr") == "0";
            var colors = ["#ff0000", "#ffd700", "#00ff00"];
            for (var lang in data['array']) {
                var $baselang = $("#" + lang).parent();
                //alert($("#" + lang).parent().lastChild);
                //var $more = $baselang.lastChild;
                for (var i = 0; i < data['array'][lang].length; i++) {
                    var $word = $("<div/>", { class: "wordline" });
                    var $input = $("<div/>", { class: "cell word" }).html(data['array'][lang][i][0]['word']).appendTo($word);
                    $input = $("<div/>", { class: "cell transcript" }).html("[" + data['array'][lang][i][0]['transcription'] + "]").appendTo($word);
                    $input = $("<div/>", { class: "cell translate" }).html(data['array'][lang][i][0]['meaning']).appendTo($word);
                    //$input = $("<div/>", { class: "cell percent" }).html(data['array'][lang][i][1].toFixed(1) + "%").appendTo($word);
                    var percent = data['array'][lang][i][1].toFixed(1);
                    $input = $("<div/>", { class: "progressbar" });
                    var $ch = $("<div/>", { width: percent }).css("background-color", colors[parseInt(percent / 34)]).appendTo($input);
                    $input.appendTo($word);
                    //$baselang.insertBefore($word, $baselang.lastChild);
                    $baselang.append($word);
                }
                $("#more_" + lang).appendTo($baselang);
                //$more.appendTo($baselang);
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


function cloneNode1(node) {
    // If the node is a text node, then re-create it rather than clone it
    var clone = node.nodeType == 3 ? document.createTextNode(node.nodeValue) : node.cloneNode(false);

    // Recurse     
    var child = node.firstChild;
    while (child) {
        clone.appendChild(cloneNode1(child));
        child = child.nextSibling;
    }

    return clone;
}