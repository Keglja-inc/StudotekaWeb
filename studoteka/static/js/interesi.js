$(document).ready(function(){
	
	var podaciIzvor = [];
	var podaciOdrediste = [];
	var zadnjeDohvacanjeIzvor = [];
	var zadnjeDohvacanjeOdrediste = [];
	$(".loadingOverlay").css("display", "block");

	$('#msg').puigrowl();

	$('#pick').puipicklist({
		filter : true,
		sourceCaption : "Dostupni interesi",
		targetCaption : "Odabrani interesi",
		sourceData : podaciIzvor,
		targetData : podaciOdrediste,
		content : function(option){
			return '<span style="float:right, font-size: 14px"><input type="hidden" value="'+ option.value +'"/>' + option.label + '<span>';
			//return option;
		},
		transfer : function(event, ui){
			var it = ui.items[0].innerText;
			//console.log(it);
			if(ui.from[0].previousSibling.innerText == "Odabrani interesi"){
				//console.log("Micem iz odabranih u ponudjene")
				for (i=0; i<podaciOdrediste.length; i++){
					if (podaciOdrediste[i].label == it){
						podaciIzvor.push(podaciOdrediste[i]);
						podaciOdrediste.splice(i, 1);
					}
				}
				
			}
			else{
				//console.log("Micem iz ponudjenih u odabrane")
				for (i=0; i<podaciIzvor.length; i++){
					if (podaciIzvor[i].label == it){
						podaciOdrediste.push(podaciIzvor[i]);
						podaciIzvor.splice(i, 1);
					}
				}
			}
		}
	}); 

	dohvatiPodatke();
	
	function dohvatiPodatke(){
		podaciIzvor = [], podaciOdrediste = [];
		$.ajax({
			url : "/rest/2e909d26d5ec066ebb42a3eb6389c1411f3b5d74"
		}).done(function(data){
			$.each(data.podaci, function(item){
				podaciIzvor.push({"label" : data.podaci[item].naziv , "value" : data.podaci[item].idInteresa }); 
			});
			zadnjeDohvacanjeIzvor = podaciIzvor.slice(0, podaciIzvor.length); //radi usporedbe razlike
			$('#pick').puipicklist('option', 'sourceData', podaciIzvor);
			$(".loadingOverlay").css("display", "none");
		}).fail(function(){
			console.log("Neuspješno dohvaćanje podataka izvora");
		});

		$.ajax({
			url : "/rest/caaf0ca037e2e3264afbafdfc3c69b95c878dac6"
		}).done(function(data){
			$.each(data.podaci, function(item){
				podaciOdrediste.push({"label" : data.podaci[item].naziv , "value" : data.podaci[item].idInteresa }); 
			});
			zadnjeDohvacanjeOdrediste = podaciOdrediste.slice(0, podaciOdrediste.length);
			$('#pick').puipicklist('option', 'targetData', podaciOdrediste);
		}).fail(function(){
			console.log("Neuspješno dohvaćanje podataka odredista");
		});;
	}


	$("#btnspremi").click(function(){
		
		var difOdredisteDel = $(zadnjeDohvacanjeOdrediste).not(podaciOdrediste).get();
		var difOdredisteAdd = $(podaciOdrediste).not(zadnjeDohvacanjeOdrediste).get();
		
		var saljiDel = [];
		var saljiAdd = [];

		for (i=0; i<difOdredisteDel.length; i++){
			saljiDel.push(difOdredisteDel[i].value);
		}
		for (i=0; i<difOdredisteAdd.length; i++){
			saljiAdd.push(difOdredisteAdd[i].value);
		}
		
		$.ajax({
			type : "POST",
			url : "/rest/052913f65b5b31417c4ca8740ea799cea8b1417b",
			contentType : "application/json; charset=utf-8",
			dataType : 'json',
			data : JSON.stringify({"idLista" : saljiAdd})
		}).done(function(msg){
			$('#msg').puigrowl('show', [{severity: "info", summary: msg.status, detail: msg.message}]);
		}).fail(function (msg){
			$('#msg').puigrowl('show', [{severity: "error", summary: msg.status, detail: msg.message}]);
		}).always(function(msg){
			dohvatiPodatke();
		});
			
		$.ajax({
			type : "POST",
			url : "/rest/7339216846bf1e056325acc6e97f4540bd8698c5",
			contentType : "application/json; charset=utf-8",
			dataType : 'json',
			data : JSON.stringify({"idLista" : saljiDel})
		}).done(function(msg){
			
		}).fail(function (msg){
			
		});
});

$("#btndodaj").click(function(){
		$.ajax({
			type : "POST",
			url : "/rest/316f625b9e0dce032a49e3385cd4cfa1f1a7787a",
			contentType : "application/json; charset=utf-8",
			dataType : 'json',
			data : JSON.stringify({"naziv" : $("#naziv").val()})
		}).done(function(msg){
			$('#msg').puigrowl('show', [{severity: "info", summary: msg.status, detail: msg.message}]);
			$("#naziv").val("")
		}).fail(function (msg){
			$('#msg').puigrowl('show', [{severity: "error", summary: msg.status, detail: msg.message}]);
		}).always(function(msg){
			dohvatiPodatke();
		});
});

});



