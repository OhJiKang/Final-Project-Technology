document.getElementById("uploadForm").addEventListener("submit", function (event) {
    event.preventDefault();
    const formData = new FormData();
    const fileInput = document.getElementById("fileInput");
    const kInput = document.getElementById("kInput").value;
    formData.append("file", fileInput.files[0]);
    formData.append("k", kInput);

    fetch("/visualize_graph_2", {
        method: "POST",
        body: formData,
    })
        .then((response) => response.json())
        .then((graph) => {
            if (graph.error) {
                alert(graph.error);
                return;
            }

            // Clear previous SVG content
            d3.select("#graph").selectAll("*").remove();

            const width = document.getElementById("graph").clientWidth;
            const height = 800;
            const svg = d3
                .select("#graph")
                .attr("width", width)
                .attr("height", height)
                .call(
                    d3.zoom().on("zoom", (event) => {
                        svg.attr("transform", event.transform);
                    })
                )
                .append("g");

            // Define a color scale with categorical colors
            const colorScale = d3.scaleOrdinal(d3.schemeCategory10);

            const simulation = d3
                .forceSimulation(graph.nodes)
                .force(
                    "link",
                    d3
                        .forceLink(graph.links)
                        .id((d) => d.id)
                        .distance(150)
                ) // Adjust distance for separation
                .force("charge", d3.forceManyBody().strength(-400)) // Increase repulsion force
                .force("center", d3.forceCenter(width / 2, height / 2));

            const link = svg
                .append("g")
                .selectAll("path")
                .data(graph.links)
                .enter()
                .append("path")
                .attr("class", "link")
                .attr("stroke", (d) => colorScale(d.color))
                .attr("stroke-width", 2);

            const node = svg
                .append("g")
                .selectAll("circle")
                .data(graph.nodes)
                .enter()
                .append("circle")
                .attr("class", "node")
                .attr("r", 10)
                .attr("fill", (d) => colorScale(d.id))
                .call(d3.drag().on("start", dragstarted).on("drag", dragged).on("end", dragended));

            const text = svg
                .append("g")
                .selectAll("text")
                .data(graph.nodes)
                .enter()
                .append("text")
                .attr("dy", -3)
                .attr("text-anchor", "middle")
                .text((d) => d.id);

            simulation.on("tick", () => {
                link.attr("d", positionLink);
                node.attr("transform", positionNode);
                text.attr("transform", positionNode);
            });

            function positionLink(d) {
                const offset = 30;
                const midpoint_x = (d.source.x + d.target.x) / 2;
                const midpoint_y = (d.source.y + d.target.y) / 2;
                const dx = d.target.x - d.source.x;
                const dy = d.target.y - d.source.y;
                const normalise = Math.sqrt(dx * dx + dy * dy);
                const offSetX = midpoint_x + offset * (dy / normalise);
                const offSetY = midpoint_y - offset * (dx / normalise);
                return `M${d.source.x},${d.source.y}S${offSetX},${offSetY} ${d.target.x},${d.target.y}`;
            }

            function positionNode(d) {
                return `translate(${d.x},${d.y})`;
            }

            function dragstarted(event, d) {
                if (!event.active) simulation.alphaTarget(0.3).restart();
                d.fx = d.x;
                d.fy = d.y;
            }

            function dragged(event, d) {
                d.fx = event.x;
                d.fy = event.y;
            }

            function dragended(event, d) {
                if (!event.active) simulation.alphaTarget(0);
                d.fx = null;
                d.fy = null;
            }
        });
});
