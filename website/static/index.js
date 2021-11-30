function deleteReport(report_id) {
  fetch("/delete-report", {
    method: "POST",
    body: JSON.stringify({ report_id: report_id }),
  }).then((_res) => {
    window.location.href = "/search-patient";
  })
  ;
}

function downloadReport(report_id) {
  fetch("/download-report", {
    method: "POST",
    body: JSON.stringify({ report_id: report_id }),
  }).then((_res) => {
    window.location.href = "/";
  });
}