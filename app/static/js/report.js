

google.charts.load('current', {packages: ['corechart', 'line']});
function drawCurveTypes(chart_data) {
    var data = new google.visualization.DataTable();
    data.addColumn('number', 'X');
    data.addColumn('number', 'Actual');
    data.addColumn({type: 'string', role: 'tooltip', 'p': {'html': true}});
    data.addColumn('number', 'Expected');
  	data.addColumn({type: 'string', role: 'tooltip', 'p': {'html': true}});

    data.addRows(chart_data);
    var options = {
        title: "Benford's Law",
        titleAlignment: "center",
        width: 900,
        height: 400,
        tooltip: {
            isHtml: true
        },
        hAxis: {
            title: 'First digit',
            viewWindow: {
                min: 0,
                max: 9
            },
            ticks: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        },
        vAxis: {
          title: 'Probability',
            format: "percent",
            viewWindow: {
              max:1.0,
                min:0.0
            }
          },
        series: {
            1: {
                curveType: 'function'
            },
            2: {
                curveType: 'function'
            }
            },
        legend: {
            position: 'top',
            alignment: 'center'
        },
        theme: 'material'
    };

   var chart = new google.visualization.LineChart(document.getElementById('chart_div'));
   chart.draw(data, options);
}
