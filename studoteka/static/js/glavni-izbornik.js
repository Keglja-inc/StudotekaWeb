$(document).ready(function(){
	$(element(1)).removeClass("active");
	var link = document.URL.split("/");
	console.log(link[link.length-1]);
	switch(link[link.length-1]){
		case "profil":
			$(element(2)).addClass("active");
			break;
	}
});
function element(x){
	return "#bs-sidebar-navbar-collapse-1 > ul > li:nth-child("+x+")";
}
