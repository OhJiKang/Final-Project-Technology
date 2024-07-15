$(document).ready(() => {
  let numOfItems = 2;
  let nameofItemsClicked = "";
  $(".locked_submit_items_num").click((event) => {
    event.preventDefault();

    $("#numOfItem").attr("readonly", true);
    numOfItems = $("#numOfItem").val();
    $(".find_recommended_items_btn").attr("disabled", false);
    $(".locked_submit_items_num").text("Change Num Of Item");
    $(".locked_submit_items_num")
      .removeClass("locked_submit_items_num")
      .addClass("unlocked_submit_items_num");
  });
  function clickAvailableBadge() {
    nameofItemsClicked = $(this).text();
    $(this).removeClass("bg-primary").addClass("bg-success");
  }

  $(".unlocked_submit_items_num").click((event) => {
    event.preventDefault();

    $("#numOfItem").attr("readonly", false);
    $(".find_recommended_items_btn").attr("disabled", true);
    $(".unlocked_submit_items_num").text("Submit Num Of Item");

    $(".unlocked_submit_items_num")
      .removeClass("unlocked_submit_items_num")
      .addClass("locked_submit_items_num");
  });

  $(".find_recommended_items_btn").click(() => {
    const formData = new FormData();
    const fileInput = document.getElementById("fileupload");
    formData.append("file", fileInput.files[0]);
    formData.append("num_of_item", $("#numOfItem").val());
    formData.append("item", nameofItemsClicked);
    $.ajax({
      url: "/finding_best_recommendation",
      type: "POST",
      data: formData,
      processData: false,
      contentType: false,
      success: function (data) {
        const resultDiv = $("#result");
        if (data.error) {
          resultDiv.html(`<p style="color: red;">${data.error}</p>`);
        } else {
          resultDiv.html(`<pre>${JSON.stringify(data, null, 2)}</pre>`);
        }
      },
    });
  });
  $(".submit_analyze").click(() => {
    const formData = new FormData();
    const fileInput = document.getElementById("fileupload");
    formData.append("file", fileInput.files[0]);
    $.ajax({
      url: "/get_unique_items_from_files",
      type: "POST",
      data: formData,
      processData: false,
      contentType: false,
      success: function (data) {
        $(".item_container").html("");
        let htmls = "";
        if (!data.error) {
          data.forEach((element, index) => {
            htmls += `<span class="badge bg-primary available_choosing" id=${index} style="margin-right:8px">${element}</span>`;
          });
          $(".item_container_choosing").html(htmls);
          $("#recommendationForm").show();
          $(".item_container_choosing").on(
            "click",
            ".available_choosing",
            clickAvailableBadge
          );
        }
      },
    });
  });
});
