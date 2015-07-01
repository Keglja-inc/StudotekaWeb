$(document).ready(function(){
	$(".loadingOverlay").css("display", "none");
	$("#container > div > div > div.panel-body > div > div > div.col-md-2.col-md-offset-1 > button").hide().click(function(event){
		alert("TODO upload slike!");
	});
	$("#container > div > div > div.panel-body > div > div > div.col-md-2.col-md-offset-1").hover(function(event){
		$("#container > div > div > div.panel-body > div > div > div.col-md-2.col-md-offset-1 > button").toggle();
		
	});
	$("#btnPosalji").click(function(event){
		$('#msg').puigrowl();
		$.ajax({
			url : "/azurirajProfil",
			type : "POST",
			data : $("form").serialize()
		}).done(function(data){
			var tip = "warning";
			if(data.status == "OK")
				tip = "info";
			$('#msg').puigrowl('show', [{severity: tip, summary: data.status, detail: data.message}]);
		}).fail(function(error){
			if(error.status == "Greška")
				$('#msg').puigrowl('show', [{severity: "error", summary: error.status, detail: error.message}]);
			else
				$('#msg').puigrowl('show', [{severity: "error", summary: "Greška", detail: "Neuspjelo ažuriranje!"}]);
		});
	});
});