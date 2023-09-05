(function($) {
    "use strict";
    jQuery(document).on('ready', function() {

        // Email Send Pie Chart
        if (document.getElementById("emailSend-chart")) {
            var emailSendChart = document.getElementById("emailSend-chart");
            var tasksCountAppel = parseFloat(emailSendChart.getAttribute("data-tasks-count-appel"));
            var tasksCountMail = parseFloat(emailSendChart.getAttribute("data-tasks-count-mail"));
            var tasksCountInterne = parseFloat(emailSendChart.getAttribute("data-tasks-count-interne"));

            var options = {
                chart: {
                    type: 'donut',
                    height: 340,
                },
                labels: ['Appel reçu', 'Mail', 'Interne'],
                series: [tasksCountAppel, tasksCountMail, tasksCountInterne],
                colors: ['#6956CE', '#1CD3D2', '#4788ff'],
                dataLabels: {
                    enabled: false,
                },
                responsive: [{
                    breakpoint: 480,
                    options: {
                        legend: {
                            position: 'bottom'
                        }
                    }
                }]
            }
            var chart = new ApexCharts(
                document.querySelector("#emailSend-chart"),
                options
            );
            chart.render();
        }

    });
}(jQuery));
