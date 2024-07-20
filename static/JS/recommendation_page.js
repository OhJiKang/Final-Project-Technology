$(document).ready(() => {
    let nameofItemsClicked = [];

    function clickAvailableBadge() {
        nameofItemsClicked.push($(this).text());
        $(this)
            .removeClass("available_choosing")
            .addClass("available_cancel");
    }
    function removeClikedBadge() {
        removedItems = $(this).text();
        nameofItemsClicked = jQuery.grep(nameofItemsClicked, function (value) {
            return value != nameofItemsClicked;
        });
        $(this)
            .removeClass("available_cancel")
            .addClass("available_choosing");
    }

    $(".find_recommended_items_btn").click(() => {
        const formData = new FormData();
        const fileInput = document.getElementById("fileupload");
        formData.append("file", fileInput.files[0]);
        formData.append("num_of_item", nameofItemsClicked.length);
        formData.append("item", nameofItemsClicked);
        $.ajax({
            url: "/finding_best_recommendation",
            type: "POST",
            data: formData,
            processData: false,
            contentType: false,
            success: function (data) {
                if (!data.error) {
                    let htmls = "";
                    data.consequent.forEach((element, index) => {
                        htmls += `<span class="bg-success recommended_item_result" id=${index} style="margin-right:8px">${element}</span>`;
                    });
                    $(".item_recommended").html(htmls);
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
                        htmls += `<span class="bg-info available_choosing" id=${index}>${element}</span>`;
                    });
                    $(".item_container_choosing").html(htmls);
                    $("#recommendationForm").show();
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
                }
            },
        });
    });
});
