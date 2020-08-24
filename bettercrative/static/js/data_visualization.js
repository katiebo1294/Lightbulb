//get id of chart
var canvas = document.getElementById("basicChart");
//type of chart
var ctx = canvas.getContext('2d');
var chartType = 'bar';
var myBasicChart;
var chart_labels = [];
var chart_data = [];

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

//initiates myBasicChart with its type, data and options
function init() {
  myBasicChart = new Chart(ctx, {
    type: chartType,
    data: data,
    options: options
  });
};

//charts.js create_chart has been moved to in html due to the use of jinja2

//refreshes the chart, later to be changed to auto update either after every
//submit or every 10 sec or 1 min
//Parameters: chart_labels: list of elements for labels
function create_chart(url, quiz_id, class_id) {
  // use python to calculate the data
  console.log("creating chart...");
  wait_and_create_chart();
  $.ajax({
    type: "GET",
    data: { 'quiz_id': quiz_id,
            'class_id': class_id },
    url: url,
    error: function (response) {
      alert(response.statusText);
      console.log(response.statusText);
    },
    success: function () {
      console.log("sent info");
    }
  });
};

async function wait_and_create_chart() {
  console.log("waiting for json");
  try {
    await get_chart_from_python();
    data = {
      labels: chart_labels,
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
        data: chart_data,
        spanGaps: true,
      }]
    };
    console.log('Attempting to create a chart');
    init();
    console.log('success');
  } catch (error) {
    console.log('failed to create chart');
    return null;
  }
}

// recieves data from a GET request given by python, it returns a tuple of labels[0] and data[1]
async function get_chart_from_python() {
  console.log("waiting to recieve chart data");
  await fetch('/calculate_chart_data')
    .then(function(response) {
      return response.json();
    }).then(function (json) {
      console.log('GET response recieved, data incoming');
      chart_labels = json[0];
      chart_data = json[1];
    });
}