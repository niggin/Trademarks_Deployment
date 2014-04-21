$(document).ready(function () {
	loadToggles();
	/*
	 Lang onclick event
	 */
    
    loadListeners();
});

function loadToggles() {
    $.fn.focuseOn = function(){
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
    }

}

function loadListeners() {
    $("#search_button").click(function () {
        fetch($("#findme").val());
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
        var $switcher = $(".onoffswitch-inner.chooselang");
        if($(this).is(":checked"))
            $switcher.each(function() {
                setUrlAttr("lt", window.getComputedStyle(this,':before').content);
            });
        else
            $switcher.each(function() {
                setUrlAttr("lt", window.getComputedStyle(this,':after').content);
            });
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
        success: function() {
            sortByMatch($("#selected_lang").html());
            $("#loader").css("display", "none");
            $("#output").css("display", "block");
        }
    });
}

function fetch(kind) {
    cleanup();
    var request = $.ajax({
        url: "/search",
        type: "GET",
        data: { findme: kind, translate: getAttrFromUrl("lt"), langs: getAttrFromUrl("lf"), sort: getAttrFromUrl("sort") },
        dataType: "json",
        beforeSend: function() { 
            $("#output").css("display", "none");
            $("#loader").css("display", "");
        },
        success: function (data) {
            for (var lang in data['array']) {
               
                var $baselang = $("<div/>", { class: "lang" });
                var $lang = $("<div/>", { class: "lang_link", id: lang }).appendTo($baselang);

                for (var i = 0; i < data['array'][lang].length; i++) {
                    var $word = $("<div/>", { class: "wordline" });
                    var $input = $("<div/>", { class: "cell word" }).html(data['array'][lang][i][0]['word']).appendTo($word);
                    $input = $("<div/>", { class: "cell transcript" }).html("[" + data['array'][lang][i][0]['ipa'] + "] " + data['array'][lang][i][0]['transcription']).appendTo($word);
                    $input = $("<div/>", { class: "cell translate" }).html(data['array'][lang][i][0]['meaning']).appendTo($word);
                    $input = $("<div/>", { class: "cell percent" }).html(data['array'][lang][i][1] + "%").appendTo($word);
                    $baselang.append($word);
                }
                $("#output").append($baselang);
            }
            if ($.isEmptyObject(data['array'])) {
                cleanup();
            } else {
                getReady();
            }
            $("#loader").css("display", "none");
            $("#output").html("").css("display", "block");
        }
    });
}


function sortByMatch() {
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
                    allwords.push(temparray[i]);
            }
        }

        allwords.sort(function (a, b) {
            var aord = a.children[2].innerHTML;
            var bord = b.children[2].innerHTML;
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

        $baselang.append("<div class='wordline lang-header'><div class='cell word'>All languages</div><div class='cell more'>more</div></div>");

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
        $(this).parent().focuseOn();
    });

    $(".lang-header .word").click(function () {
        $(this).parent().focuseOn();
    });
}

function fetch_more(lang_out) {
    var request = $.ajax({
        url: "/load_more",
        type: "GET",
        data: { lang: lang_out.id },
        dataType: "json",
        success: function(data) {
            for (var lang in data['array']) {
                var $baselang = $("#" + lang).parent();
                for (var i = 0; i < data['array'][lang].length; i++) {
                    var $word = $("<div/>", { class: "wordline" });
                    var $input = $("<div/>", { class: "cell word" }).html(data['array'][lang][i][0]['word']).appendTo($word);
                    $input = $("<div/>", { class: "cell transcript" }).html("[" + data['array'][lang][i][0]['transcription'] + "]").appendTo($word);
                    $input = $("<div/>", { class: "cell translate" }).html(data['array'][lang][i][0]['meaning']).appendTo($word);
                    $input = $("<div/>", { class: "cell percent" }).html(data['array'][lang][i][1] + "%").appendTo($word);
                    $baselang.append($word);
                    if (data['hide_morebutton'][lang]) {
                        $("#button_" + lang).css("display", "none");
                    }
                }
            }
        }
    });
}