$(function charts () {
    $.ajax({
        url: window.location.pathname,
        type: 'get',
        success: function (response) {
            console.log(response["demod"])
            new Morris.Line({
                // ID of the element in which to draw the chart.
                element: 'velocitychart',
                // Chart data records -- each entry in this array corresponds to a point on
                // the chart.
                data: response["velocity"],
                // The name of the data record attribute that contains x-values.
                xkey: 'created',
                // A list of names of data record attributes that contain y-values.
                ykeys: ['velocity'],
                // Labels for the ykeys -- will be displayed when you hover over the
                // chart.
                labels: ['DE VERTICAL', 'NDE HORIZONTAL', 'NDE VERTICAL', 'DE HORIZONTAL']
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
                ykeys: ['acelaration'],
                // Labels for the ykeys -- will be displayed when you hover over the
                // chart.
                labels: ['DE VERTICAL', 'NDE HORIZONTAL', 'NDE VERTICAL', 'DE HORIZONTAL']
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
                ykeys: ['demod_spectrum'],
                // Labels for the ykeys -- will be displayed when you hover over the
                // chart.
                labels: ['DE VERTICAL', 'NDE HORIZONTAL', 'NDE VERTICAL', 'DE HORIZONTAL']
            })
        }
    })
})



//new Morris.Line({
    // ID of the element in which to draw the chart.
//    element: 'myfirstchart',
    // Chart data records -- each entry in this array corresponds to a point on
    // the chart.
//    data: [
//        {y: '2021', a: 50},
//        {y: '2022', a: 65},
//        {y: '2023', a: 50},
//        {y: '2024', a: 75},
//        {y: '2025', a: 80},
//        {y: '2026', a: 70},
//        {y: '2027', a: 100},
//        {y: '2028', a: 115},
//        {y: '2029', a: 120},
//        {y: '2030', a: 145},
//        {y: '2031', a: 160},
//    ],
    // The name of the data record attribute that contains x-values.
//    xkey: 'y',
    // A list of names of data record attributes that contain y-values.
//    ykeys: ['a'],
    // Labels for the ykeys -- will be displayed when you hover over the
    // chart.
//    labels: ['Value']
//})
