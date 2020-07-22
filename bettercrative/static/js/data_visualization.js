//get id of chart
var canvas = document.getElementById("basicChart");
//type of chart
var ctx = canvas.getContext('2d');
var chartType = 'bar';
var myBasicChart;

//temp data
var tempdata = {
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

//data
var data = {
  labels: ["True", "False"],
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
    data: [0, 0],
    spanGaps: true,
    }]
  };

//options for chart
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
      text: 'Demo',
      position: 'bottom'
    }
  };

//initial initialization
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
//Parameters: numTrue: number of true responses
//            numFalse: number of false responses
function create_chart(numTrue, numFalse) {
  data = {
  labels: ["True", "False"],
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
    data: [numTrue, numFalse],
    spanGaps: true,
    }]
  };
        console.log('Attempting to create a chart');
        init();
        console.log('success');

};