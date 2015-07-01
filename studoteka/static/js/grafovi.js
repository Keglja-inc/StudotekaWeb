$(document).ready(function(){
	
	
});

$("#btnPrioriteti").click(function(){
	$.ajax({
		url: "/rest/f10b84c033e39eb4298c01d05cd1b6cabcb45158",
		type : "GET",
		contentType : "application/json"
	}).done(function(data){
		podaci = [];
		for(i=0; i<data.podaci.length;i++){
			podaci.push(data.podaci[i]);
		}
		podaciZaGraf = {
			"labels" : ["1. prioritet", "2. prioritet", "3. prioritet", "4. prioritet", "5. prioritet"],
			"datasets" : [
			      {
			    	  "label": "Prioriteti prema fakultetima",
			          "fillColor": "rgba(151,187,205,0.5)",
			          "strokeColor": "rgba(151,187,205,0.8)",
			          "highlightFill": "rgba(151,187,205,0.75)",
			          "highlightStroke": "rgba(151,187,205,1)",
			          "data": podaci
			      }
			]
		};
		if($("#graf").length){
			$("#graf").remove();
		}
		$("#desno").append('<canvas id="graf" width="400" height="400"></canvas>');
		
		var ctx = document.getElementById("graf").getContext("2d");
		var myNewChart = new Chart(ctx).Bar(podaciZaGraf, barOptions);	
	}).fail(function(data){

	});
});

$("#btnPostoci").click(function(){
	$.ajax({
		url: "/rest/5beabefdf587548578e92f28f07e3c435e574bf7",
		type : "GET",
		contentType : "application/json"
	}).done(function(data){
		podaci = [], labele = [];
		for(i=0; i<data.podaci.length;i++){
			podaci.push(data.podaci[i].broj);
			labele.push(data.podaci[i].postotak);
		}
		podaciZaGraf = {
			"labels" : labele,
			"datasets" : [
			      {
			    	  "label": "Prioriteti prema fakultetima",
			          "fillColor": "rgba(151,187,205,0.5)",
			          "strokeColor": "rgba(151,187,205,0.8)",
			          "highlightFill": "rgba(151,187,205,0.75)",
			          "highlightStroke": "rgba(151,187,205,1)",
			          "data": podaci
			      }
			]
		};
		if($("#graf").length){
			$("#graf").remove();
		}
		$("#desno").append('<canvas id="graf" width="400" height="400"></canvas>');
		
		var ctx = document.getElementById("graf").getContext("2d");
		var myNewChart = new Chart(ctx).Line(podaciZaGraf, lineOptions);	
	}).fail(function(data){

	});
});

$("#btnTop10").click(function(){
	$.ajax({
		url: "/rest/f4af7f520c332ab2a3b8fe9a8ccd0cb9e4e65ffc",
		type : "GET",
		contentType : "application/json"
	}).done(function(data){
		podaci = [], labele = [];
		for(i=0; i<data.podaci.length;i++){
			podaci.push(data.podaci[i].broj);
			labele.push(data.podaci[i].naziv);
		}
		podaciZaGraf = {
			"labels" : labele,
			"datasets" : [
			      {
			    	  "label": "Prioriteti prema fakultetima",
			          "fillColor": "rgba(151,187,205,0.5)",
			          "strokeColor": "rgba(151,187,205,0.8)",
			          "highlightFill": "rgba(151,187,205,0.75)",
			          "highlightStroke": "rgba(151,187,205,1)",
			          "data": podaci
			      }
			]
		};
		if($("#graf").length){
			$("#graf").remove();
		}
		$("#desno").append('<canvas id="graf" width="400" height="400"></canvas>');
		
		var ctx = document.getElementById("graf").getContext("2d");
		var myNewChart = new Chart(ctx).Bar(podaciZaGraf, barOptions);	
	}).fail(function(data){

	});
});