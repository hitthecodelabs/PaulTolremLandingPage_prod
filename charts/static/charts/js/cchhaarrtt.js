
async function initializeData() {
    // Fetch the timezone offset
    timezoneOffset = fetchTimezoneOffset();

    // Start updating chart data
    updateChartDataPeriodically();
}

const tooltip = d3.select("#chart")
    .append("div")
    .attr("class", "tooltip")
    .style("opacity", 0);

async function loadChartData() {

    // Fetch the timezone offset
    const timezoneOffset = fetchTimezoneOffset();

    // Fetch the new data
    const symbol0 = document.getElementById("symbol").value.toLowerCase().replace("usdt", "");
    const newApiUrl = "/api/get_xtimes_preds/" + symbol0;
    let newData;
    try {
        const response = await fetch(newApiUrl, {
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        });
        const result = await response.json();
        newData = result.result.map(d => ({ date: new Date(+d[0] + timezoneOffset), value: +d[1] }));
    } catch (error) {
        console.error("Error fetching new data:", error);
    }

    const apiUrl = "https://fapi.binance.com/fapi/v1/klines";
    const symbol = document.getElementById("symbol").value;
    const selectedTimeframe = document.getElementById("timeframe").value;
    const interval = selectedTimeframe;
    const limit = 360;
    const fullUrl = apiUrl + "?symbol=" + symbol + "&interval=" + interval + "&limit=" + limit;
    const candleWidth = 1.75;

    fetch(fullUrl)
        .then(response => response.json())
        .then(data => {
    const processedData = data.map(d => ({
    // Apply the timezone offset to the date
    date: new Date(d[0] + timezoneOffset),
    open: +d[1],
    high: +d[2],
    low: +d[3],
    close: +d[4],
    pchange: +(100 * (d[4] - d[1]) / d[1]).toFixed(2),
    pamplitude: +(100 * (d[2] - d[3]) / d[3]).toFixed(2),
    bullish: d[4] >= d[1],
}));

            d3.select("#chart").selectAll("g").remove();

            const margin = { top: 20, right: 100, bottom: 120, left: 55 };
            const width = 960 - margin.left - margin.right;
            const height = 500 - margin.top - margin.bottom;
/**
            const x = d3.scaleUtc()
                .domain([d3.min(processedData, d => d.date.getTime() - candleWidth / 2), d3.max(processedData, d => d.date.getTime() + candleWidth / 2)])
                .range([margin.left, width - margin.right]);
*/

            const x = d3.scaleUtc()
                .domain([d3.min([...processedData, ...newData], d => d.date.getTime() - candleWidth / 2), d3.max([...processedData, ...newData], d => d.date.getTime() + candleWidth / 2)])
                .range([margin.left, width - margin.right]);

            const y = d3.scaleLinear()
                .domain([d3.min(processedData, d => d.low), d3.max(processedData, d => d.high)])
                .range([height - margin.bottom, margin.top]);

            // Create a new y-axis for the new data
            const y2 = d3.scaleLinear()
                .domain([0, 1])
                .range([height - margin.bottom, margin.top]);

            const xAxis = g => g
                .attr("transform", `translate(0,${height - margin.bottom})`)
                .call(d3.axisBottom(x).ticks(width / 80).tickSizeOuter(0));

            const lastClose = processedData[processedData.length - 1].close;
            const lastDate = processedData[processedData.length - 1].date;
            const yAxis = g => g
                .attr("transform", `translate(${margin.left},0)`)
                .call(d3.axisLeft(y))
                .call(g => g.select(".domain").remove()) 
                .call(g => g.select(".tick:last-of-type text").clone()
                    .attr("x", 4)
                    .attr("text-anchor", "start")
                    .attr("font-weight", "bold")
                    .text(`Price (USD) $${lastClose}`));

            const yAxis2 = g => g
                .attr("transform", `translate(${width - margin.right},0)`)
                .call(d3.axisRight(y2))
                .call(g => g.select(".domain").remove())
                .call(g => g.select(".tick:last-of-type text").clone()
                    .attr("x", -6)
                    .attr("text-anchor", "end")
                    .attr("font-weight", "bold")
                    .text(`AI Momentum`));

            let svg = d3.select("#chart").select("svg");
            if (svg.empty()) {
                svg = d3.select("#chart").append("svg")
                    .attr("viewBox", [0, 0, width, height])
                    .on("mousemove", mousemove)
                    .on("mouseout", mouseout);
            } else {
                svg.selectAll("*").remove();
            }

            const g = svg.append("g")
                .attr("stroke-linecap", "round")
                .attr("stroke", "black")
                .selectAll("g")
                .data(processedData)
                .join("g")
                .attr("transform", d => `translate(${x(d.date)},0)`)
                .attr("data-date", d => d.date.getTime()) 
                .on("mouseover", mouseover)
                .on("mousemove", mousemove)
                .on("mouseout", mouseout);

            const wickWidth = 0.15;
            g.append("rect")
                .attr("x", -wickWidth / 2)
                .attr("y", d => y(d.high))
                .attr("width", wickWidth)
                .attr("height", d => y(d.low) - y(d.high))
                .attr("fill", d => d.bullish ? "green" : "red")
                .attr("rx", 1)
                .attr("ry", 1);

            g.append("rect")
                .attr("x", -candleWidth / 2)
                .attr("y", d => y(Math.max(d.open, d.close)))
                .attr("width", candleWidth)
                .attr("height", d => Math.max(1, Math.abs(y(d.open) - y(d.close)))) // Set a minimum height of 1
                .attr("fill", d => d.bullish ? "green" : "red")
                .attr("rx", 1)
                .attr("ry", 1);

            // New g selection for the line data
            const lineGroup = svg.append("g");
            
            newData.forEach(function (d) {
                let newValue = d.value < 0.5 ? 1 - d.value : d.value;
                let strokeColor = newValue < 0.66 ? "gray" : d.value < 0.5 ? "red" : "green";
            
                lineGroup.append("line")
                    .attr("x1", x(d.date))
                    .attr("y1", y2(0)) // start at 0 on y2 axis
                    .attr("x2", x(d.date))
                    .attr("y2", y2(newValue))
                    .attr("stroke", strokeColor)
                    .attr("stroke-width", 1.0)
                    .attr("opacity", 0.33); // 50% opacity

                lineGroup.append("line")
                    .attr("x1", x(d.date))
                    .attr("y1", y2(0)) // start at 0 on y2 axis
                    .attr("x2", x(d.date))
                    .attr("y2", y2(1))
                    .attr("stroke", strokeColor)
                    .attr("stroke-width", 1.0)
                    .attr("opacity", 0.15); // 50% opacity
            });

            // console.log("x domain:", x.domain());
            // console.log("newData dates:", newData.map(d => d.date.getTime()));


            // Define an array of offsets for the vertical lines
            let lineOffsets = [-candleWidth / 2, 0, candleWidth / 2];

            svg.append("g")
                .call(xAxis);

            svg.append("g")
                .call(yAxis);

            svg.append("g")
                .call(yAxis2);


            function mouseover(d) {
                tooltip.style("opacity", 1);
            }

            function mouseout() {
                tooltip.style("opacity", 0);
            }
        })
        .catch(error => {
            console.error("Error fetching data:", error);
        });
}

function updateChartDataPeriodically() {
    loadChartData();
    // setTimeout(updateChartDataPeriodically, 10000); 
    setTimeout(updateChartDataPeriodically, 30000); 
}

// updateChartDataPeriodically();
// Call the initialization function
initializeData();

document.getElementById("timeframe").addEventListener("change", loadChartData);
document.getElementById("symbol").addEventListener("change", loadChartData);

function mousemove(event, d) {
    try {
        if (!d) throw new Error('Data is undefined');
        tooltip
            .html(`<table>
                <tr><td>Date:  </td><td>${d.date.toISOString().split('.')[0].replace("T", " ")}</td></tr>
                <tr><td>Open:  </td><td>${d.open}</td></tr>
                <tr><td>High:  </td><td>${d.high}</td></tr>
                <tr><td>Low:  </td><td>${d.low}</td></tr>
                <tr><td>Close:  </td><td>${d.close}</td></tr>
                <tr><td>% Change:  </td><td>${d.pchange.toFixed(2)}%</td></tr>
                <tr><td>% Amplitude:  </td><td>${d.pamplitude.toFixed(2)}%</td></tr>
            </table>`)
            .style("left", (event.pageX + 15) + "px")
            .style("top", (event.pageY - 28) + "px");
    } catch (e) {
        // console.error(e);
    }
}