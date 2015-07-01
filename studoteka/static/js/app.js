$(document).ready(function(){
	$(".loadingOverlay").css("display", "none");

	var postojiAktivan = false;
	$("#bs-sidebar-navbar-collapse-1 > ul > li").each(function(event){
		if ($(this).hasClass("active")){
			postojiAktivan = true;
		}
		$(this).removeClass("active");
	});
	if(!postojiAktivan){
		$($("#bs-sidebar-navbar-collapse-1 > ul > li")[0]).addClass("active");
		dohvatiSucelje("pocetna");
	}

	$("#bs-sidebar-navbar-collapse-1 > ul > li a").click(function(event){
		$("#bs-sidebar-navbar-collapse-1 > ul > li").each(function(event){
			$(this).removeClass("active");
		});
		$($(this).context.parentElement).addClass("active");
		
		var veza = $(this).context.innerText.toLowerCase();
		if(veza!="postavke"){
			dohvatiSucelje(veza);
		}
	});
});

function dohvatiSucelje(veza){
	$.ajax({
		url: "/"+veza
	}).done(function(data){
		$("#container").empty();
		$("#container").html(data);	
	}).fail(function(){
		$("#container").empty();
		$("#container").html("No data received!");
		$(".loadingOverlay").css("display", "none");
	});
}
