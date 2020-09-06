/*
  Description: Holds two charts.js canvas's, One is for general quiz info, other for specific question info, such as percentages of each answer chosen.
  All appears on the results page
*/

//get id of chart
var canvas = document.getElementById("basicChart");
var question_canvas = document.getElementById("question_data");
//type of chart
var results_ctx = canvas.getContext('2d');
var question_ctx = question_canvas.getContext('2d');

var questionDataChart;
var myBasicChart;
var chart_labels = [];
var chart_data = [];
var myLineExtend = Chart.controllers.line.prototype.draw;

Chart.pluginService.register({
  beforeDraw: function(chart) {
    // checks if the current chart is the question one
    if(chart.config.options.isquestion_ctx)
    {
      var width = chart.chart.width,
          height = chart.chart.height,
          question_ctx = chart.chart.ctx;

      question_ctx.restore();
      var fontSize = (height / 150).toFixed(2);
      question_ctx.font = fontSize + "em sans-serif";
      question_ctx.textBaseline = "middle";

      // change this variable to modify what is stated in the text area
      var text = "No Question Selected",
          textX = Math.round((width - question_ctx.measureText(text).width) / 2),
          textY = height / 2;

        question_ctx.fillText(text, textX, textY);
        question_ctx.save();
      
    }
  }
});

init_question(undefined, undefined, 'pie');
init(undefined, undefined, 'bar');

//initiates myBasicChart with its type, data and options
function init(data, title_text, chartType) {
  if (data == undefined) {
    myBasicChart = new Chart(results_ctx, {
      type: chartType,
      data: {
        labels: [""],
        datasets: [{
          label: "No Chart Selected",
        }]
      },
      options: {
        isquestion_ctx: false,
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
  else if (chartType == 'doughnut') {
    myBasicChart = new Chart(results_ctx, {
      type: chartType,
      data: data,
      options: {
        isquestion_ctx: false,
        scales: {
          xAxes: [{
            display:false
          }]
        },
        title: {
          fontSize: 18,
          display: true,
          text: title_text,
          position: 'bottom'
        }
      }
    });
  }
  else {
    myBasicChart = new Chart(results_ctx, {
      type: chartType,
      data: data,
      options: {
        isquestion_ctx: false,
        scales: {
          yAxes: [{
            ticks: {
              beginAtZero: true,
              suggestedMax: y_min
            }
          }]
        },
        title: {
          fontSize: 18,
          display: true,
          text: title_text,
          position: 'bottom'
        }
      }
    });
  }
};

//initiates questionDataChart with its type, data and options
function init_question(data, title_text, chartType) {
  if (data == undefined) {
    questionDataChart = new Chart(question_ctx, {
      type: chartType,
      data: {
        labels: [""],
        datasets: [{
          label: "No Chart Selected",
        }],
      },
      options: {
        isquestion_ctx: true,
        scales: {
          xAxes: [{
            display:false
          }]
        },
        title: {
          fontSize: 18,
          display: true,
          text: 'Select a Question',
          position: 'bottom'
        },
      },
    });
  }
  else {
    questionDataChart = new Chart(question_ctx, {
      type: chartType,
      data: data,
      options: {
        isquestion_ctx: false,
        scales: {
          xAxes: [{
            display:false
          }]
        },
        title: {
          fontSize: 18,
          display: true,
          text: title_text,
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
function create_chart(url, quiz_id, class_id, chart_type) {
  // use python to calculate the data
  myBasicChart.destroy();
  console.log("creating chart..." + class_id + quiz_id + " ");
  $.ajax({
    type: "GET",
    data: {
      'quiz_id': quiz_id,
      'class_id': class_id,
      'chart_type': chart_type
    },
    url: url,
    error: function (response) {
      alert(response.statusText);
      console.log(response.statusText);
    },
    success: function (data) {
      console.log("sent info");
      console.log("waiting for json");
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
        
        // If its a doughnut, set each color to something different
        if(chart_type == 'doughnut')
        {
          var i;
          var doughnut_array = [];
          var color;
          title_text = "Correct Question Responses";
          for(i=0;i<=chart_labels.length;i++)
          {
            color = Math.floor((Math.abs(Math.sin(i) * 16777215)) % 16777215);
            color = color.toString(16);
            // pad any colors shorter than 6 characters with leading 0s
            while(color.length < 6) {
                color = '0' + color;
            }
            doughnut_array.push("#"+color);
          }
          data = {
            labels: chart_labels,
            datasets: [{
              label: "Student Scores",
              fill: true,
              lineTension: 0.1,
              backgroundColor: doughnut_array,
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
        }
        else
        {
          title_text = "Student Responses";
        }

        console.log('Attempting to create a chart');
        init(data, title_text, chart_type);
        console.log('success');
      } catch (error) {
        console.log('failed to create chart');
        console.log(error);
        return null;
      }


    }
  });
};


function create_question_chart(url, quiz_id, class_id, question_id, q_num) {
  // use python to calculate the data
  questionDataChart.destroy();
  console.log("creating question chart..." + class_id + quiz_id + question_id + " ");
  $.ajax({
    type: "GET",
    data: {
      'quiz_id': quiz_id,
      'class_id': class_id,
      'question_id': question_id
    },
    url: url,
    error: function (response) {
      alert(response.statusText);
      console.log(response.statusText);
    },
    success: function (data) {
      console.log("sent info");
      console.log("waiting for json");
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

        var i;
        var pie_array = [];
        var color;
        title_text = "Question" + q_num;
        for(i=0;i<=chart_labels.length;i++)
        {
          color = Math.floor((Math.abs(Math.sin(i) * 16777215)) % 16777215);
          color = color.toString(16);
          // pad any colors shorter than 6 characters with leading 0s
          while(color.length < 6) {
              color = '0' + color;
          }
          pie_array.push("#"+color);
        }
        data = {
          labels: chart_labels,
          datasets: [{
            label: "Student Scores",
            fill: true,
            lineTension: 0.1,
            backgroundColor: pie_array,
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
        init_question(data, title_text, 'pie');
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

    // if no answers have been graded, class total will show NaN; this prevents that from happening
    if(!isNaN(class_total)) {
        this.innerHTML = class_total + "%";
    }
});

// changes the active quiz displayed in result
function change_active_result(url,q_id,c_id)
{
  $.ajax({
    type: "GET",
    data: {
      'q_id': q_id,
      'c_id': c_id
    },
    url: url,
    error: function (response) {
      alert(response.statusText);
      console.log(response.statusText);
    },
    success: function () {
      console.log("changed active result quiz");
      refresh("#results_display")
    }
  });
}