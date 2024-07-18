document
  .getElementById("uploadForm")
  .addEventListener("submit", function (event) {
    event.preventDefault();
    const formData = new FormData();
    const fileInput = document.getElementById("fileInput");
    formData.append("file", fileInput.files[0]);

    fetch("/get_unique_items_from_files", {
      method: "POST",
      body: formData,
    })
      .then((response) => response.json())
      .then((graphdata) => {
        let htmls = "";
        if (graphdata.error) {
          alert(graphdata.error);
          return;
        } else {
          graphdata.forEach((element, index) => {
            htmls += `<span class="badge bg-primary available_choosing" id=${index} style="margin-right:8px">${element}</span>`;
          });
          $(".item_container_choosing").html(htmls);
        }
      });
  });
