function init() {
    var data = [];
    d3.request("http://127.0.0.1:5000/all").get(response => {

        data = JSON.parse(response.response);

        var yearNumber = [];
        var countryName = [];
        var monthNumber = [];
        var magnitudeNumber = [];
        var depthNumber = [];
        var yearList = [];
        var dummyArray = [];
        var latitudeValues = [];
        var longitudeValues = [];
        var minorArray = [];
        var lightArray = [];
        var moderateArray = [];
        var strongArray = [];
        var majorArray = [];
        var greatArray = [];
        var yearArray = [];

        var minorCnt = 0;
        var lightCnt = 0;
        var moderateCnt = 0;
        var strongCnt = 0;
        var majorCnt = 0;
        var greatCnt = 0;

        for (var i = 0; i < data.length; i++) {

            if (!yearNumber.includes(data[i].Year)) {
                yearNumber.push(data[i].Year);
            }

            if (!countryName.includes(data[i].Name)) {
                countryName.push(data[i].Name)
            }

            if (!monthNumber.includes(data[i].Month)) {
                monthNumber.push(data[i].Month)
            }

            magnitudeNumber.push(parseFloat(data[i].Magnitude));
            depthNumber.push(parseFloat(data[i].Depth));
            yearList.push(parseInt(data[i].Year));
            dummyArray.push(parseInt(1));
            latitudeValues.push(data[i].Latitude);
            longitudeValues.push(data[i].Longitude);

            if (i === 0) {
                yearArray.push(data[i].Year);
                if (data[i].Magnitude >= 3.0 && data[i].Magnitude < 4.0) {
                    minorCnt += 1;
                }
                else if (data[i].Magnitude >= 4.0 && data[i].Magnitude < 5.0) {
                    lightCnt += 1;
                }
                else if (data[i].Magnitude >= 5.0 && data[i].Magnitude < 6.0) {
                    moderateCnt += 1;
                }
                else if (data[i].Magnitude >= 6.0 && data[i].Magnitude < 7.0) {
                    strongCnt += 1;
                }
                else if (data[i].Magnitude >= 7.0 && data[i].Magnitude < 8.0) {
                    majorCnt += 1;
                }
                else if (data[i].Magnitude >= 8.0) {
                    greatCnt += 1;
                }
            }
            else if (i === data.length - 1) {
                minorArray.push(minorCnt);
                lightArray.push(lightCnt);
                moderateArray.push(moderateCnt);
                strongArray.push(strongCnt);
                majorArray.push(majorCnt);
                greatArray.push(greatCnt);
            }
            else if (yearArray.includes(data[i].Year)) {
                if (data[i].Magnitude >= 3.0 && data[i].Magnitude < 4.0) {
                    minorCnt += 1;
                }
                else if (data[i].Magnitude >= 4.0 && data[i].Magnitude < 5.0) {
                    lightCnt += 1;
                }
                else if (data[i].Magnitude >= 5.0 && data[i].Magnitude < 6.0) {
                    moderateCnt += 1;
                }
                else if (data[i].Magnitude >= 6.0 && data[i].Magnitude < 7.0) {
                    strongCnt += 1;
                }
                else if (data[i].Magnitude >= 7.0 && data[i].Magnitude < 8.0) {
                    majorCnt += 1;
                }
                else if (data[i].Magnitude >= 8.0) {
                    greatCnt += 1;
                }
            }
            else {
                minorArray.push(minorCnt);
                lightArray.push(lightCnt);
                moderateArray.push(moderateCnt);
                strongArray.push(strongCnt);
                majorArray.push(majorCnt);
                greatArray.push(greatCnt);
                
                minorCnt = 0;
                lightCnt = 0;
                moderateCnt = 0;
                strongCnt = 0;
                majorCnt = 0;
                greatCnt = 0;

                if (data[i].Magnitude >= 3.0 && data[i].Magnitude < 4.0) {
                    minorCnt += 1;
                }
                else if (data[i].Magnitude >= 4.0 && data[i].Magnitude < 5.0) {
                    lightCnt += 1;
                }
                else if (data[i].Magnitude >= 5.0 && data[i].Magnitude < 6.0) {
                    moderateCnt += 1;
                }
                else if (data[i].Magnitude >= 6.0 && data[i].Magnitude < 7.0) {
                    strongCnt += 1;
                }
                else if (data[i].Magnitude >= 7.0 && data[i].Magnitude < 8.0) {
                    majorCnt += 1;
                }
                else if (data[i].Magnitude >= 8.0) {
                    greatCnt += 1;
                }

                yearArray.push(data[i].Year)
            }

        }

        yearNumber.forEach(year => {
            var sel = document.getElementById('datetime');
            var opt = document.createElement('option');
            opt.appendChild(document.createTextNode(year));
            opt.value = year;
            sel.appendChild(opt);
        })

        countryName.forEach(country => {
            var sel = document.getElementById('country');
            var opt = document.createElement('option');
            opt.appendChild(document.createTextNode(country));
            opt.value = country;
            sel.appendChild(opt);
        })

        monthNumber.forEach(month => {
            var sel = document.getElementById('month');
            var opt = document.createElement('option');
            opt.appendChild(document.createTextNode(country));
            opt.value = month;
            sel.appendChild(opt);
        })

        var magnitudeMax = Math.max.apply(null, magnitudeNumber.filter(function(n) { return !isNaN(n); }));
        var depthAverage = math.mean.apply(null, depthNumber.filter(function(n) { return !isNaN(n); })).toFixed(2);
        var earthquakeCount = yearList.length;

        // Then, select the unordered list element by class name
        var list = d3.select("#maxmag");

        // remove any children from the list to
        list.html("");

        // append stats to the list
        list.append("li").text(`Maximum Magnitude: ${magnitudeMax}`);
        list.append("li").text(`Average Depth: ${depthAverage}`);
        list.append("li").text(`Earthquake Count: ${earthquakeCount}`);

        var trace1 = {
            x: yearList,
            y: dummyArray,
            //text: otuLabels,
            type: 'bar'
        }

        var trace2 = {
            x: magnitudeNumber,
            type: 'histogram',
        };

        var trace3 = {
            lon: longitudeValues,
            lat: latitudeValues,
            radius:10,
            z: magnitudeNumber,
            type: "densitymapbox",
            coloraxis: 'coloraxis',
            hoverinfo: 'skip'
        }

        var magnitudeMinorTrace = {
            x: yearArray,
            y: minorArray,
            name: 'Minor',
            type: 'bar'
        }


        var magnitudeLightTrace = {
            x: yearArray,
            y: lightArray,
            name: 'Light',
            type: 'bar'
        }

        var magnitudeModerateTrace = {
            x: yearArray,
            y: moderateArray,
            name: 'Moderate',
            type: 'bar'
        }

        var magnitudeStrongTrace = {
            x: yearArray,
            y: strongArray,
            name: 'Strong',
            type: 'bar'
        }

        var magnitudeMajorTrace = {
            x: yearArray,
            y: majorArray,
            name: 'Major',
            type: 'bar'
        }

        var magnitudeGreatTrace = {
            x: yearArray,
            y: greatArray,
            name: 'Great',
            type: 'bar'
        }
        var barData = [trace1];
        var histogramData = [trace2];
        var heatMapdata = [trace3];
        var magnitudeData = [magnitudeMinorTrace, magnitudeLightTrace,magnitudeModerateTrace,magnitudeStrongTrace,magnitudeMajorTrace,magnitudeGreatTrace];
        
        var layout = {
            mapbox: {center: {lon: -98.5795, lat: 39.8283}, style: "outdoors", zoom: 2},
            coloraxis: {colorscale: "Viridis"}, title: {text: "Earthquake Magnitude"},
            width: 600, height: 400, margin: {t: 30, b: 0}};

        var magnitudeLayout = {barmode: 'stack'};

        var config = {mapboxAccessToken: "pk.eyJ1Ijoic3RlZmFuZWU4OCIsImEiOiJja2Y3ZTZsNTMwMWt0MnFvNHduZGRpaDk2In0.qbfCdcHGNqgJ5QNccagpug"};

        Plotly.newPlot('bar', barData);
        Plotly.newPlot('histogram', histogramData);
        Plotly.newPlot('heatmap', heatMapdata, layout, config);
        Plotly.newPlot('stackedbar', magnitudeData, magnitudeLayout);

        });

};


init();