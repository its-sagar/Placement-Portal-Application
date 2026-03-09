// ChartJS Script
document.addEventListener("DOMContentLoaded", function () {

    const chartCanvas = document.getElementById("overviewChart");

    const totalStudents = chartCanvas.dataset.students;
    const totalCompanies = chartCanvas.dataset.companies;
    const totalDrives = chartCanvas.dataset.drives;
    const totalApplications = chartCanvas.dataset.applications;

    var ctx = chartCanvas.getContext("2d");

    new Chart(ctx, {
        type: "bar",
        data: {
            labels: ["Students", "Companies", "Drives", "Applications"],
            datasets: [{
                label: "Total Count",
                data: [
                    totalStudents,
                    totalCompanies,
                    totalDrives,
                    totalApplications
                ],
                backgroundColor: [
                    "rgba(75, 108, 183, 0.6)",
                    "rgba(11, 163, 96, 0.6)",
                    "rgba(245, 87, 108, 0.6)",
                    "rgba(79, 172, 254, 0.6)"
                ],
                borderColor: [
                    "rgba(75, 108, 183, 1)",
                    "rgba(11, 163, 96, 1)",
                    "rgba(245, 87, 108, 1)",
                    "rgba(79, 172, 254, 1)"
                ],
                borderWidth: 1,
                borderRadius: 5
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        precision: 0
                    }
                }
            },
            plugins: {
                legend: {
                    display: false
                }
            }
        }
    });

});