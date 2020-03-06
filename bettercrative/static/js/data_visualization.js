//Code for data_visualization
var canvas = document.getElementById("basicChart");
var ctx = canvas.getContext('2d');

var chartType = 'bar';
var myBasicChart;

//temp data
var data = {
    labels: ["student1", "student2", "student3", "student4", "student5", "student6", "student7", "student8", "student9", "student10", "student11", "student12"],
    datasets: [{
      label: "Student Scores",
      fill: true,
      lineTension: 0.1,
      backgroundColor: "rgba(0,255,0,0.4)",
      borderColor: "green", // The main line color
      borderCapStyle: 'square',
      pointBorderColor: "white",
      pointBackgroundColor: "green",
      pointBorderWidth: 1,
      pointHoverRadius: 8,
      pointHoverBackgroundColor: "yellow",
      pointHoverBorderColor: "green",
      pointHoverBorderWidth: 2,
      pointRadius: 4,
      pointHitRadius: 10,
      data: [10, 13, 17, 12, 30, 47, 60, 120, 230, 300, 310, 400],
      spanGaps: true,
  }]
};


var options = {
    scales: {
      yAxes: [{
        ticks: {
          beginAtZero: true
        }
      }]
    },
    title: {
      fontSize: 18,
      display: true,
      text: 'Look How Dumb',
      position: 'bottom'
    }
  };

init();

//initiates myBasicChart with its type, data and options
function init() {
    myBasicChart = new Chart(ctx, {
        type: chartType,
        data: data,
        options: options
      });
};

//refreshes the chart, later to be changed to auto update either after every
//submit or every 10 sec or 1 min
function create_chart() {
        console.log('Attempting to create a chart');
        init();

};
//


// function toggleChart() {
//   //destroy chart:
//   myBarChart.destroy();
//   //change chart type: 
//   this.chartType = (this.chartType == 'bar') ? 'line' : 'bar';
//   //restart chart:
//   init();
// }