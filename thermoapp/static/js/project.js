new Morris.Line(
{
    element: 'line-chart',
    data: [
        {y: '2021', a: 50},
        {y: '2022', a: 65},
        {y: '2023', a: 50},
        {y: '2024', a: 75},
        {y: '2025', a: 80},
        {y: '2026', a: 70},
        {y: '2027', a: 100},
        {y: '2028', a: 115},
        {y: '2029', a: 120},
        {y: '2030', a: 145},
        {y: '2031', a: 160},
    ],
        xkey: 'y',
        ykey: ['a'],
        labels: ['Total Income'],
        pointFillColors: ['#ffffff'],
        pointStrokeColors : ['black']
})
