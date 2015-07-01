$(document).ready(function() {
    $('#example').dataTable( {
        "processing": true,
        "serverSide": true,
        "ajax": "/rest/9786583ec82eaf5bac6d070e104a6661a45033a1",
        "columns": [
            { "data": "idZapisa" },
            { "data": "vrijeme" },
            { "data": "idLogiranogKorisnika" },
            { "data": "tipLogiranogKorisnika" },
            { "data": "akcija" }
        ]
    } );
} );