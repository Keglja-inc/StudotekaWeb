$(document).ready(function(){
	var server = "http://stufac.us.wak-apps.com";
	var podaciIzvor = [];
	var podaciOdrediste = [];
	var zadnjeDohvacanjeIzvor = [];
	var zadnjeDohvacanjeOdrediste = [];
	
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
			url : server+"/interesi?fakultetID="+ $("#id").val() + "&invert=true"
		}).done(function(data){
			$.each(data.podaci, function(item){
				podaciIzvor.push({"label" : data.podaci[item].naziv , "value" : data.podaci[item].idInteresa }); 
			});
			zadnjeDohvacanjeIzvor = podaciIzvor.slice(0, podaciIzvor.length); //radi usporedbe razlike
			$('#pick').puipicklist('option', 'sourceData', podaciIzvor);
		}).fail(function(){
			console.log("Neuspješno dohvaćanje podataka izvora");
		});

		$.ajax({
			url : server+"/interesi?fakultetID="+ $("#id").val()
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
			data : JSON.stringify(saljiAdd)
		}).done(function(msg){
			console.log(msg);
			//$$(getHtmlId("rtxtPoruka")).setValue(msg.message);
			//$("#"+getHtmlId("rtxtPoruka")).css({"color":"green"});
		}).fail(function (msg){
			//$$(getHtmlId("rtxtPoruka")).setValue(msg.message);
			//$("#"+getHtmlId("rtxtPoruka")).css({"color":"red"});
		}).always(function(msg){
			dohvatiPodatke();
		});
			/*
		$.ajax({
			type : "POST",
			url : "/rest/",
			contentType : "application/json; charset=utf-8",
			dataType : 'json',
			data : JSON.stringify(saljiDel)
		}).done(function(msg){
			console.log(msg);
			//$$(getHtmlId("rtxtPoruka")).setValue(msg.message);
			//$("#"+getHtmlId("rtxtPoruka")).css({"color":"green"});
		}).fail(function (msg){
			//$$(getHtmlId("rtxtPoruka")).setValue(msg.message);
			//$("#"+getHtmlId("rtxtPoruka")).css({"color":"red"});
		});*/
	});

	$("#btndodaj").click(function(){
		var podatak = [];
		console.log("ASDHAHSJHJSD");
		//podatak.push($("#naziv").val());
		console.log($("#naziv").val());
		/*
		$.ajax({
			type : "POST",
			url : "/rest/052913f65b5b31417c4ca8740ea799cea8b1417b",
			contentType : "application/json; charset=utf-8",
			dataType : 'json',
			data : JSON.stringify(podatak)
		}).done(function(msg){
			console.log(msg);
			//$$(getHtmlId("rtxtPoruka")).setValue(msg.message);
			//$("#"+getHtmlId("rtxtPoruka")).css({"color":"green"});
		}).fail(function (msg){
			//$$(getHtmlId("rtxtPoruka")).setValue(msg.message);
			//$("#"+getHtmlId("rtxtPoruka")).css({"color":"red"});
		}).always(function(msg){
			dohvatiPodatke();
		});*/
	});

});



