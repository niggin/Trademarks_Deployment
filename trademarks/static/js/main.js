$(document).ready(function() {
	loadToggles();
	/*
	 Lang onclick event
	 */
	$(".lang_link").click(function() {
		$(this).focuseOn();
	});
	$("#search_button").click(function () {
	    fetch(document.getElementById('findme1').value);
	});
	$("#findme1").keyup(function (event) {
	    if (event.keyCode == 13) {
	        $("#search_button").click();
	    }
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
    var $sort_b = $("#percent_button");
    $sort_b.toggleClass('active');
    sortByMatch();
}

function fetch(kind) {
    var request = $.ajax({
        url: "/search_sortbymatch",
        type: "GET",
        data: { findme: kind },
        dataType: "json",
        success: function(json) {
            cleanup();
            var group = document.getElementById('output');
            group.innerHTML = "";
            group.setAttribute("style", "display:block");
            for (var VAR in json['array']) {
                var baselang = document.createElement("div");
                baselang.setAttribute("class", "lang");
                baselang.setAttribute("id", "lang1");
                var lang = document.createElement("div");
                lang.setAttribute("class", "lang_link");
                lang.id = VAR;
                baselang.appendChild(lang);
                for (var i = 0; i < json['array'][VAR].length; i++) {
                    var word = document.createElement("div");
                    word.setAttribute("class", "wordline");
                    var input = document.createElement("div");
                    input.setAttribute("class", "cell word");
                    input.innerHTML = json['array'][VAR][i][0]['word'];
                    word.appendChild(input);
                    input = document.createElement("div");
                    input.setAttribute("class", "cell transcript");
                    input.innerHTML = "[" + json['array'][VAR][i][0]['ipa'] + "]";
                    word.appendChild(input);
                    input = document.createElement("div");
                    input.setAttribute("class", "cell translate");
                    input.innerHTML = json['array'][VAR][i][0]['meaning'];
                    word.appendChild(input);
                    input = document.createElement("div");
                    input.setAttribute("class", "cell percent");
                    input.innerHTML = json['array'][VAR][i][1] + "%";
                    word.appendChild(input);
                    baselang.appendChild(word);
                }
                group.appendChild(baselang);
            }
            if (jQuery.isEmptyObject(json['array'])) {
                cleanup();
            } else {
                getreadey();
            }
        }
    });
}


function sortByMatch() {
    var source = document.getElementById('output');
    var tohide = document.getElementById("tohide");
    if (tohide.innerHTML != "") {
        source.innerHTML = "";
        source.innerHTML = tohide.innerHTML;
        tohide.innerHTML = "";
    } else {
        var group = Array.prototype.slice.call(source.children, 0);
        var myArray = new Array();
        for (var item in group) {
            var temparray = Array.prototype.slice.call(group[item].children, 0);
            for (var i = 1; i < temparray.length; i++) {
                myArray.push(temparray[i]);
            }
        }

        myArray.sort(function (a, b) {
            var aord = a.children[3].innerHTML;
            var bord = b.children[3].innerHTML;
            return parseInt(bord) - parseInt(aord);
        });
        tohide.innerHTML = source.innerHTML;
        group = document.getElementById('output');
        group.innerHTML = "";
        var baselang = document.createElement("div");
        baselang.setAttribute("class", "lang");
        baselang.setAttribute("id", "lang1");
        var lang = document.createElement("div");
        lang.setAttribute("class", "lang_link");
        lang.id = "all";
        baselang.appendChild(lang);
        for (i = 0; i < myArray.length; i++) {
            baselang.appendChild(myArray[i]);
        }
        group.appendChild(baselang);
    }
    getreadey();
}

function cleanup() {
    document.getElementById("results-header").setAttribute("style", "display:none");
    document.getElementById("tohide").innerHTML = "";
}

function getreadey() {
    document.getElementById("results-header").setAttribute("style", "");
    $(".lang_link").click(function () {
        $(this).focuseOn();
    });
}