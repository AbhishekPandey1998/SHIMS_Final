function deleteReport(report_id, patient_id) {
  fetch("/delete-report", {
    method: "POST",
    body: JSON.stringify({ report_id: report_id, patient_id: patient_id }),
  }).then((_res) => {
     window.location.href = "/patient-details-and-reports/"+patient_id;
  });
}

function downloadReport(report_id, patient_id) {
  fetch("/download-report", {
    method: "POST",
    body: JSON.stringify({ report_id: report_id, patient_id: patient_id}),
  }).then((_res) => {
    window.location.href = "/download-report/"+patient_id+"/"+report_id;
  });
}