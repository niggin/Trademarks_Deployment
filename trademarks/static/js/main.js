$(document).ready(function() {
	loadToggles();
	/*
	 Lang onclick event
	 */

	$("#search_button").click(function () {
        fetch($("#findme").val());
	});

	$("#findme").keyup(function (event) {
	    if (event.keyCode == 13) {
	        $("#search_button").click();
	    }
	});

    $(".percent_button").click(function () {
        sort();
    });

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

function sort() {
    $(".percent_button").toggleClass('active');
    $.ajax({
        beforeSend: function() {
            $("#output").css("display", "none");
            $("#loader").css("display", "");
        },
        success: function() {
            sortByMatch();
            $("#loader").css("display", "none");
            $("#output").css("display", "block");
        }
    });
}

function fetch(kind) {
    cleanup();
    var request = $.ajax({
        url: "/search_sortbymatch",
        type: "GET",
        data: { findme: kind },
        dataType: "json",
        beforeSend: function() { 
            $("#output").css("display", "none");
            $("#loader").css("display", "");
        },
        success: function (data) {
            for (var lang in data['array']) {
               
                var $baselang = $("<div/>", { class: "lang", id: "lang1" });
                var $lang1 = $("<div/>", { class: "lang_link", id: lang }).appendTo($baselang);

                for (var i = 0; i < data['array'][lang].length; i++) {
                    var $word = $("<div/>", { class: "wordline" });
                    var $input = $("<div/>", { class: "cell word" }).html(data['array'][lang][i][0]['word']).appendTo($word);
                    $input = $("<div/>", { class: "cell transcript" }).html("[" + data['array'][lang][i][0]['ipa'] + "] " + data['array'][lang][i][0]['transcription']).appendTo($word);
                    $input = $("<div/>", { class: "cell translate" }).html(data['array'][lang][i][0]['meaning']).appendTo($word);
                    $input = $("<div/>", { class: "cell percent" }).html(data['array'][lang][i][1] + "%").appendTo($word);
                    $baselang.append($word);
                }
                console.log(data);
                $("#output").append($baselang);
            }
            if ($.isEmptyObject(data['array'])) {
                cleanup();
            } else {
                getReady();
                $("#results-header").css("display", "");
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
            for (var i = 1; i < temparray.length; i++) {
                allwords.push(temparray[i]);
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

        for (i = 0; i < allwords.length; i++) {
            $baselang.append(allwords[i]);
        }

        $source.append($baselang);
    }

    getReady();
    
}

function cleanup() {
    $("#results-header").css("display", "none");
    $("#loader").css("display", "none");
    if ($("#tohide").html().localeCompare("")) {
        $("#tohide").html("");
        $(".percent_button").toggleClass('active');
    }
    $("#output").html("");
}

function getReady() {
    $("#results-header").css("display", "");
    $(".lang_link").click(function () {
        $(this).focuseOn();
    });
}