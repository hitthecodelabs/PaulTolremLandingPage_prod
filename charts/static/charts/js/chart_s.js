let chart;
let candleSeries;
let timezoneOffset;
let histogramSeries;
let lighterHistogramSeries;

let binanceDataInterval;
let serverDataInterval;

function fetchTimezoneOffset() {
    var timezone = Intl.DateTimeFormat().resolvedOptions().timeZone;
    var offsetInMinutes = moment().tz(timezone).utcOffset();
    var offsetInMilliseconds = offsetInMinutes * 60 * 1000;
    return offsetInMilliseconds / 1000;
}

function createChart() {
    chart = LightweightCharts.createChart(document.getElementById('chart'), {
        // width: document.body.clientWidth,
        width: 1100,
        height: 425,
        priceScale: {
            position: 'right',
        },
        timeScale: {
            timeVisible: true,
            secondsVisible: false,
        },
    });

    candleSeries = chart.addCandlestickSeries();
    // lineSeries = chart.addLineSeries(); // add a line series
    histogramSeries = chart.addHistogramSeries({
        priceScaleId: 'newData',
        color: 'rgba(255, 165, 0, 0.5)',
        priceScale: {
            position: 'right',
            drawTicks: false,
        },
    });

    lighterHistogramSeries = chart.addHistogramSeries({
        priceScaleId: 'newData',
        priceScale: {
            position: 'right',
            drawTicks: false,
        },
    });
}

async function initializeData() {
    // Fetch the timezone offset
    timezoneOffset = fetchTimezoneOffset();

    // Create the chart
    createChart();

    // Start updating chart data
    updateBinanceDataPeriodically();
    updateServerDataPeriodically();
}

document.addEventListener("DOMContentLoaded", initializeData);

function processJsonData(data) {
    return data
        .filter(d => d.every(value => value !== null && value !== undefined))
        .map(d => ({
            time: (d[0] / 1000) + timezoneOffset,
            open: +d[1],
            high: +d[2],
            low: +d[3],
            close: +d[4]
        }));
}

const symbolDropdown = document.getElementById("symbol");
const intervalDropdown = document.getElementById("timeframe");

// Loading Binance data
async function loadBinanceData() {

    const selectedSymbol = symbolDropdown.options[symbolDropdown.selectedIndex].value;
    const selectedInterval = intervalDropdown.options[intervalDropdown.selectedIndex].value;

    // Get the user's timezone
    const timezone = Intl.DateTimeFormat().resolvedOptions().timeZone;

    // Determine the location based on the client's timezone
    let location = 'com';

    // List of US and Canada timezones
    const usCanadaTimezones = ['America/New_York','America/Detroit',
        'America/Kentucky/Louisville','America/Kentucky/Monticello',
        'America/Indiana/Indianapolis','America/Indiana/Vincennes',
        'America/Indiana/Winamac','America/Indiana/Marengo',
        'America/Indiana/Petersburg','America/Indiana/Vevay',
        'America/Chicago','America/Indiana/Tell_City','America/Indiana/Knox','America/Menominee',
        'America/North_Dakota/Center','America/North_Dakota/New_Salem',
        'America/North_Dakota/Beulah','America/Denver','America/Boise','America/Phoenix',
        'America/Los_Angeles','America/Anchorage','America/Juneau','America/Sitka',
        'America/Metlakatla','America/Yakutat','America/Nome','America/Adak','Pacific/Honolulu'
    ];

    if (usCanadaTimezones.includes(timezone)) {
        location = 'us';
    }

    // time is in milliseconds
    let currentTime = Date.now();

    // Construct the URL for the server API call
    const apiUrl = `/api/get_chart_data/${selectedSymbol}/${selectedInterval}/${currentTime}/${location}/`;

    // Make the server API call
    const response = await fetch(apiUrl, {
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
            // 'Authorization': `Token ${userToken}`
        }
    });
    const data = await response.json();

    if (data.error) {
        console.error("Error fetching data:", data.error);
        return;
    }

    const processedData = processJsonData(data);
    const seen = new Set();
    const uniqueData = processedData.filter(el => {
        const duplicate = seen.has(el.time);
        seen.add(el.time);
        return !duplicate;
    });

    // Update the data of the candleSeries
    candleSeries.setData(uniqueData);

    // Update status box
    if (uniqueData.length > 0) {
        const lastDataPoint = uniqueData[uniqueData.length - 1];
        document.getElementById('statusBox').innerHTML = `
            <b>Symbol:</b> ${selectedSymbol} &nbsp;&nbsp;
            <b>Interval:</b> ${selectedInterval} &nbsp;&nbsp;
            <b>Open:</b> ${lastDataPoint.open.toFixed(2)} &nbsp;&nbsp;
            <b>High:</b> ${lastDataPoint.high.toFixed(2)} &nbsp;&nbsp;
            <b>Low:</b> ${lastDataPoint.low.toFixed(2)} &nbsp;&nbsp;
            <b>Close:</b> ${lastDataPoint.close.toFixed(2)}
        `;
    }

}

// Loading server data
async function loadServerData() {

    const selectedSymbol = symbolDropdown.options[symbolDropdown.selectedIndex].value;
    const selectedInterval = intervalDropdown.options[intervalDropdown.selectedIndex].value;

    // Fetch the new data
    const ApiUrl = "/api/get_xtimes_preds/" + selectedSymbol.toLowerCase().replace("usdt", "") + "/" + selectedInterval;
    // const ApiUrl = `/api/get_xtimes_preds/${selectedSymbol.toLowerCase().replace("usdt", "")}/${selectedInterval}/`;
    // const ApiUrl = "http://127.0.0.1:8880/api/get_xtimes_preds/" + selectedSymbol.toLowerCase().replace("usdt", "");
    let newData;
    try {
        const response = await fetch(ApiUrl, {
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                // 'Authorization': `Token ${userToken}`
            }
        });
        const result = await response.json();
        // newData = result.result.map(d => ({ time: (d[0] / 1000), value: +d[1] }));
        newData = result.result.map(d => ({ time: (d[0] / 1000) + timezoneOffset, value: +d[1] }));
        // newData = result.result.map(d => ({ time: new Date(+d[0] + timezoneOffset), value: +d[1] }));
    } catch (error) {
        console.error("Error fetching new data:", error);
    }

    const pastelRed = 'rgba(252, 0, 255, 1)';
    // const pastelGreen = 'rgba(0, 255, 255, 1)';
    const pastelGreen = 'rgba(0, 215, 255, 1)';

    // const pastelRed = 'rgba(255, 105, 97, 1)';
    // const pastelGreen = 'rgba(152, 251, 152, 1)';
    // const pastelGreen = 'rgba(34, 139, 34, 1)';
    // const pastelGreen = 'rgba(76, 187, 23, 1)';
    const gray = 'rgba(128, 128, 128, 1)';

    let grayP = 0.000001;

    histogramSeries.setData(newData.map(d => {
        // Convert the original values to new ones
        let newValue = d.value < 0.5 ? 1 - d.value : d.value;
        // let strokeColor = newValue < 0.500001 ? pastelRed : d.value < 0.5 ? pastelRed : pastelGreen;
        let strokeColor = d.value < 0.5 - grayP ? pastelRed : (d.value >= (0.5-grayP) && d.value < (0.5 + grayP)) ? gray : pastelGreen;

        // Compute opacity
        // let opacity = 0.10 + (((newValue - 0.5) * 2) * 0.45);
        let opacity = 0.45;

        // Convert number to string and keep 2 decimal places
        opacity = opacity.toFixed(2);

        // Plot the vertical line extending from 0 to the converted value
        return {
            time: d.time,
            value: newValue * 100,
            color: strokeColor.replace('1)', opacity + ')'),
        };
    }));

    // Plot the lighter vertical lines extending from 0 to 1 on the Y-axis
    lighterHistogramSeries.setData(newData.map(d => {
        let newValue = d.value < 0.5 ? 1 - d.value : d.value;
        // let strokeColor = newValue < 0.500001 ? pastelRed : d.value < 0.5 ? pastelRed : pastelGreen;
        let strokeColor = d.value < 0.5 - grayP ? pastelRed : (d.value >= (0.5-grayP) && d.value < (0.5 + grayP)) ? gray : pastelGreen;

        return {
            time: d.time,
            value: 100,
            color: strokeColor.replace('1)', '0.10)'),
        };
    }));
}

function updateBinanceDataPeriodically() {
    loadBinanceData();
    binanceDataInterval = setInterval(loadBinanceData, 6.5 * 1000);
}

function updateServerDataPeriodically() {
    loadServerData();
    serverDataInterval = setInterval(loadServerData, 30 * 1000);
}

symbolDropdown.addEventListener("change", function() {
    clearInterval(binanceDataInterval);
    clearInterval(serverDataInterval);
    loadBinanceData();
    loadServerData();
    binanceDataInterval = setInterval(loadBinanceData, 6.5 * 1000);
    serverDataInterval = setInterval(loadServerData, 30 * 1000);
});

intervalDropdown.addEventListener("change", function() {
    clearInterval(binanceDataInterval);
    clearInterval(serverDataInterval);
    loadBinanceData();
    loadServerData();
    binanceDataInterval = setInterval(loadBinanceData, 6.5 * 1000);
    serverDataInterval = setInterval(loadServerData, 30 * 1000);
});