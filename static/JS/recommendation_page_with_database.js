$(document).ready(() => {
  let nameofItemsClicked = [];

  function clickAvailableBadge() {
    nameofItemsClicked.push($(this).text());
    $(this).removeClass("available_choosing").addClass("available_cancel");
  }
  function removeClikedBadge() {
    removedItems = $(this).text();
    let index = nameofItemsClicked.indexOf(removedItems);
    if (index > -1) {
      // Remove the element from the array
      nameofItemsClicked.splice(index, 1);
    }
    $(this).removeClass("available_cancel").addClass("available_choosing");
  }

  $(".find_recommended_items_btn").click(() => {
    const formData = new FormData();
    formData.append("num_of_item", nameofItemsClicked.length);
    formData.append("item", nameofItemsClicked);
    $.ajax({
      url: "/finding_best_recommendation_with_database",
      type: "POST",
      data: formData,
      processData: false,
      contentType: false,
      success: function (data) {
        if (data) {
          let htmls = "";
          data.consequent.forEach((element, index) => {
            htmls += `<span class="bg-success recommended_item_result" id=${index} style="margin-right:8px">${element}</span>`;
          });
          $(".item_recommended").html(htmls);
        } else {
          $(".item_recommended").html(
            `<span class="bg-danger recommended_item_result"  style="margin-right:8px">Chưa có dữ liệu thống kê</span>`
          );
        }
      },
    });
  });
  $(".item_container_choosing").on(
    "click",
    ".available_choosing",
    clickAvailableBadge
  );
  $(".item_container_choosing").on(
    "click",
    ".available_cancel",
    removeClikedBadge
  );
});
