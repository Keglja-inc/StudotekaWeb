$(document).ready(function () {
    $('#popisFakulteta').jtable({
            title: 'Popis fakulteta',
            paging : true,
            pageSize : 10,
            actions: {
                listAction: '/rest/84002239b8bb525bad1cc689fee5569d98462307',
                createAction: '/rest/5e358c3fa86341b6f7ebf1b5ac98c123bb34d38b',
                updateAction: '/rest/37cdf6db410abda9c72152491e9feccf6c3cf8db',
                deleteAction: '/rest/58978999b05a1b8ea86d2723aa717982c47ece21'
            },
            fields: {
                idFakulteta: {
                	title : "ID fakulteta",
                    key: true
                },
                naziv: {
                    title: 'Naziv fakulteta',
                    width : "100%"
                },
                ulica: {
                    title: 'Ulica'
                },
                kucniBroj: {
                    title: 'Kućni broj'
                },
                postanskiBroj :{
                    title : 'Poštanski broj'                    
                },
                mjesto: {
                    title: 'Mjesto'
                },
                kontaktEmail: {
                    title: 'Kontakt e-mail'
                },
                kontaktTelefon: {
                    title: 'Kontakt telefon'
                },
                logo : {
                    title : 'Logo'
                },
                webStranica : {
                    title : 'Internet stranica'
                },
                visokoUciliste : {
                	title : 'Visoko učilište'
                },
                email : {
                    title : "Email"
                },
                lozinka : {
                	title : "Lozinka",
                	width : "10%"
                }
            }
        });
    $('#popisFakulteta').jtable('load');
    $('body > div:nth-child(3)').addClass('smart-green')
    $('body > div:nth-child(3)').css({'border' : '1px solid'});
    $('body > div.ui-dialog.ui-widget.ui-widget-content.ui-corner-all.ui-front.ui-dialog-buttons.ui-draggable.ui-resizable.smart-green > div.ui-dialog-titlebar.ui-widget-header.ui-corner-all.ui-helper-clearfix.ui-draggable-handle').html("<h1>Dodavanje novog fakulteta</h1>");
    $('button').addClass('button')
});
    