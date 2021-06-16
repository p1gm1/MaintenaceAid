$(function charts () {
    $.ajax({
        url: window.location.pathname,
        type: 'get',
        success: function (response) {
            $('#articleTable tbody').html("")
            console.log(response["data"].length)
            for (let i = 0; i < response["data"].length; i++) {
                let row = '<tr>'
                row += '<td>' + response["data"][i]["monitoring_point"] + '</td>'
                row += '<td>' + response["data"][i]["date"] + '</td>'
                row += '<td>' + response["data"][i]["prev vel"] + '</td>'
                row += '<td>' + response["data"][i]["last vel"] + '</td>'
                row += '<td>' + response["data"][i]["prev acel"] + '</td>'
                row += '<td>' + response["data"][i]["last acel"] + '</td>'
                row += '<td>' + response["data"][i]["demod prev"] + '</td>'
                row += '<td>' + response["data"][i]["demod last"] + '</td>'
                row += '</tr>'
                $('#articleTable tbody').append(row)
            }
            $('#articleTable').DataTable({
                language: {
                    "decimal": "",
                    "emptyTable": "No hay información",
                    "info": "Mostrando _START_ a _END_ de _TOTAL_ Entradas",
                    "infoEmpty": "Mostrando 0 a 0 de 0 Entradas",
                    "infoFiltered": "(Filtrando de _MAX_ total entradas)",
                    "infoPostFix": "",
                    "thousands": ",",
                    "lengthMenu": "Mostrando _MENU_ entradas",
                    "loadingRecords": "Cargando...",
                    "processing": "Procesando...",
                    "search": "Buscar:",
                    "zeroRecords": "Sin resultados encontrados",
                    "paginate": {
                        "first": "Primero",
                        "last": "Ultimo",
                        "next": "Siguiente",
                        "previous": "Anterior"
                    },
                },
                responsive: true,
                "columns": [
                    {"data": "Punto de monitoreo"},
                    {"data": "Fecha"},
                    {"data": "Velocidad previa"},
                    {"data": "Velocidad final"},
                    {"data": "Aceleración previa"},
                    {"data": "Aceleración final"},
                    {"data": "Demod Spectrum previo"},
                    {"data": "Demod Spectrum final"}
                ],
                "columnDefs": [{
                    "targets": [2, 3, 4, 5, 6, 7],
                    render(v){
                        return Number(v).toFixed(2)
                    }
                }], 
            })
            let vel_keys = []
            let acel_keys = []
            let demod_keys = []
            for (let i = 0; i <= (response["demod"].length-1); i++) {
                try {
                    if (response["demod"][i]["monitoring_point"] != response["demod"][i+1]["monitoring_point"]) {
                        demod_keys.push(response["demod"][i]["monitoring_point"])
                    }
                } catch (TypeError) {
                    demod_keys.push(response["demod"][response["demod"].length-1]["monitoring_point"])
                }
            }
            for (let i = 0; i <= (response["velocity"].length-1); i++) {
                try {
                    if (response["velocity"][i]["monitoring_point"] != response["velocity"][i+1]["monitoring_point"]) {
                        vel_keys.push(response["velocity"][i]["monitoring_point"])
                    }
                } catch (TypeError) {
                    vel_keys.push(response["velocity"][response["velocity"].length-1]["monitoring_point"])
                }
            }
            for (let i = 0; i <= (response["acelaration"].length-1); i++) {
                try {
                    if (response["acelaration"][i]["monitoring_point"] != response["acelaration"][i+1]["monitoring_point"]) {
                        acel_keys.push(response["acelaration"][i]["monitoring_point"])
                    }
                } catch (TypeError) {
                    acel_keys.push(response["acelaration"][response["acelaration"].length-1]["monitoring_point"])
                }
            }
            new Morris.Line({
                // ID of the element in which to draw the chart.
                element: 'velocitychart',
                // Chart data records -- each entry in this array corresponds to a point on
                // the chart.
                data: response["velocity"],
                // The name of the data record attribute that contains x-values.
                xkey: 'created',
                // A list of names of data record attributes that contain y-values.
                ykeys: vel_keys,
                // Labels for the ykeys -- will be displayed when you hover over the
                // chart.
                labels: vel_keys
            })
            new Morris.Line({
                // ID of the element in which to draw the chart.
                element: 'acelarationchart',
                // Chart data records -- each entry in this array corresponds to a point on
                // the chart.
                data: response["acelaration"],
                // The name of the data record attribute that contains x-values.
                xkey: 'created',
                // A list of names of data record attributes that contain y-values.
                ykeys: acel_keys,
                // Labels for the ykeys -- will be displayed when you hover over the
                // chart.
                labels: acel_keys
            })
            new Morris.Line({
                // ID of the element in which to draw the chart.
                element: 'demodchart',
                // Chart data records -- each entry in this array corresponds to a point on
                // the chart.
                data: response["demod"],
                // The name of the data record attribute that contains x-values.
                xkey: 'created',
                // A list of names of data record attributes that contain y-values.
                ykeys: demod_keys,
                // Labels for the ykeys -- will be displayed when you hover over the
                // chart.
                labels: demod_keys
            })
        }
    })
})
