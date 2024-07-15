document.getElementById("recommendationForm").addEventListener("submit", function (event) {
    event.preventDefault();

    const formData = new FormData(this);

    fetch("/finding_best_recommendation", {
        method: "POST",
        body: formData,
    })
        .then((response) => response.json())
        .then((data) => {
            const resultDiv = document.getElementById("result");
            if (data.error) {
                resultDiv.innerHTML = `<p style="color: red;">${data.error}</p>`;
            } else {
                resultDiv.innerHTML = `<pre>${JSON.stringify(data, null, 2)}</pre>`;
            }
        })
        .catch((error) => {
            console.error("Error:", error);
            const resultDiv = document.getElementById("result");
            resultDiv.innerHTML = `<p style="color: red;">An error occurred. Please try again.</p>`;
        });
});
