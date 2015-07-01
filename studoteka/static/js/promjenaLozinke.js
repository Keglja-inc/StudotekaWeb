$("#btnPromjenaLozinke").click(function(event){
	$('#msg').puigrowl();
	$.ajax({
		url : "/promjeniLozinku",
		type : "POST",
		data : $("form").serialize()
	}).done(function(data){
		var tip = "warning";
		$("#trenutnaLozina").empty();
		$("#novaLozina").empty();
		$("#ponovljenaLozina").empty();
		if(data.status == true)
			tip = "info";
		$('#msg').puigrowl('show', [{severity: tip, summary: data.status, detail: data.message}]);
	}).fail(function(error){
		console.log("NIJEJE");
		if(error.status == false)
			$('#msg').puigrowl('show', [{severity: "error", summary: error.status, detail: error.message}]);
		else
			$('#msg').puigrowl('show', [{severity: "error", summary: "Greška", detail: "Neuspjelo ažuriranje!"}]);
	});
});