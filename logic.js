function init() {
    //d3.json("data/earthquake.json").then((data) => {
    var data = [];
    d3.request("http://127.0.0.1:5000/all").get(response => {

        data = JSON.parse(response.response);

        var yearNumber = [];

        for (var i = 0; i < data.length; i++) {

            if (!yearNumber.includes(data[i].Year)) {
                yearNumber.push(data[i].Year);
            }
        }

        console.log(yearNumber);

        yearNumber.forEach(year => {
            var sel = document.getElementById('selDataset');
            var opt = document.createElement('option');
            opt.appendChild(document.createTextNode(year));
            opt.value = year;
            sel.appendChild(opt);
        })
        });

};


init();