//get id of chart
var canvas = document.getElementById("basicChart");
//type of chart
var ctx = canvas.getContext('2d');
var chartType = 'bar';
var myBasicChart;
var chart_labels = [];
var chart_data = [];

//options for chart
var options = {
  scales: {
    yAxes: [{
      ticks: {
        beginAtZero: true,
        suggestedMax: 100
      }
    }]
  },
  title: {
    fontSize: 18,
    display: true,
    text: 'Student Responses',
    position: 'bottom'
  }
};

init(undefined);

//initiates myBasicChart with its type, data and options
function init(data) {
  if (data == undefined) {
    myBasicChart = new Chart(ctx, {
      type: chartType,
      data: {
        labels: [""],
        datasets: [{
          label: "No Chart Selected",
        }]
      },
      options: {
        scales: {
          yAxes: [{
            ticks: {
              beginAtZero: true,
              suggestedMax: 100
            }
          }]
        },
        title: {
          fontSize: 18,
          display: true,
          text: '',
          position: 'bottom'
        }
      }
    });
  }
  else {
    myBasicChart = new Chart(ctx, {
      type: chartType,
      data: data,
      options: {
        scales: {
          yAxes: [{
            ticks: {
              beginAtZero: true,
              max: y_min
            }
          }]
        },
        title: {
          fontSize: 18,
          display: true,
          text: 'Student Responses',
          position: 'bottom'
        }
      }
    });
  }
};

//charts.js create_chart has been moved to in html due to the use of jinja2

//refreshes the chart, later to be changed to auto update either after every
//submit or every 10 sec or 1 min
//Parameters: chart_labels: list of elements for labels
function create_chart(url, quiz_id, class_id) {
  // use python to calculate the data
  console.log("creating chart..." + class_id + quiz_id + " ");
  $.ajax({
    type: "GET",
    data: {
      'quiz_id': quiz_id,
      'class_id': class_id
    },
    url: url,
    error: function (response) {
      alert(response.statusText);
      console.log(response.statusText);
    },
    success: function (data) {
      console.log("sent info");
      console.log("waiting for json");
      refresh('#classroom-results')
      try {
        console.log("waiting to recieve chart data");
        console.log('GET response recieved, data incoming');
        //sets the labels and data to the data recieved from the GET request
        chart_labels = data[0];
        chart_data = data[1];
        y_min = data[2];
        console.log("labels:" + chart_labels);
        console.log("data: " + chart_data);
        console.log("min y axis: " + y_min);

        var data = {
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
          }],
          y_min: y_min
        };
        console.log('Attempting to create a chart');
        init(data);
        console.log('success');
      } catch (error) {
        console.log('failed to create chart');
        console.log(error);
        return null;
      }


    }
  });
};

// for the table's class total
$("[id^='class-total-']").each(function() {
    var q_id = this.id.slice(12);
    console.log("calculating class total for question " + q_id);

    var tableRows = $("td[id^='response-data-" + q_id + "-'] > span:not(.text-info)");
    var total_answered = tableRows.length;
    console.log("total answered = " + total_answered);
    var correctRows = $("td[id^='response-data-" + q_id + "-'] > span.text-success");
    var total_correct = correctRows.length;
    console.log("total correct = " + total_correct);
    var class_total = Math.round(total_correct/total_answered * 100);
    console.log("correctness ratio = " + total_correct + "/" + total_answered + "(" + class_total + "%)");
    this.innerHTML = class_total + "%";
});