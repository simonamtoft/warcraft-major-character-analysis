var in_labels = [  0. ,  10.2,  20.4,  30.6,  40.8,  51. ,  61.2,  71.4,  81.6, 91.8, 102. ]
var out_labels = [ 0. ,  8.4, 16.8, 25.2, 33.6, 42. , 50.4, 58.8, 67.2, 75.6, 84. ]

lineChart = new Chart(document.getElementById("InOutDeg"), {
    type: 'bar',
    data: {
        labels: out_labels,
        datasets: [{
            data: [95., 85., 43., 12., 14.,  5.,  2.,  3.,  1.,  1.],
            borderWidth: 1
        }]
    },
    options: {
        title: {
            display: true,
            text: 'Out Degree Distribution of Gcc'
        },
        legend: {
        display: false
    },
    tooltips: {
        callbacks: {
           label: function(tooltipItem) {
                  return tooltipItem.yLabel;
           }
        }
    }
    }
});


document.getElementById("Out-Degree").addEventListener("click", function() {
  lineChart.config.data = {
            labels: out_labels,
            datasets: [{
                data: [95., 85., 43., 12., 14.,  5.,  2.,  3.,  1.,  1.],

            }],
        }
        lineChart.options.title.text = "Out Degree Distribution of Gcc"
        lineChart.update();
});

document.getElementById("In-Degree").addEventListener("click", function() {
  lineChart.config.data = {
            labels: in_labels,
            datasets: [{
                data: [138.,  63.,  25.,  15.,   5.,   7.,   4.,   3.,   0.,   1.],

            }],
        }
        lineChart.options.title.text = "In Degree Distribution of Gcc"
        lineChart.update();
});
