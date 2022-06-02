/*
*    main.js
*/

var margin = {top: 10, right: 10, bottom: 100, left:100};
var width = 600;
var height = 400;

var svg = d3.select("#chart-area")
	.append("svg")
	.attr("width", width + margin.right + margin.left)
	.attr("height", height + margin.top + margin.bottom);

class ObjCont {
		constructor(name, population) {
		  this.name = name;
		  this.population = population;
		}
	  }

var g = svg.append("g")
    .attr("transform", "translate(" + margin.left + ", " + margin.top + ")");

	d3.json("../../sim/sim.json").then((data)=> {

		aux = new Map
		info = new Map
		continentes = ['africa','asia','europe','middle_east','n_america','oceania_se_asia','s_america']
		dias = ['day_0','day_1','day_2','day_3','day_4','day_5','day_6','day_7','day_8','day_9']
		console.log(data);
		Object.keys(data).forEach(day => {
			//console.log(day)
			continentes.forEach(cont => {
				//console.log(cont)
				info.set(day,aux.set(cont,data[day][cont].population))
			});

		});
		
		var populations = []
		var objsContinents = []
		
		continentes.forEach(cont => {
			populations.push(info.get(dias[0]).get(cont))
			objsContinents.push(new ObjCont(cont,info.get(dias[0]).get(cont)))
		});
		
		console.log(objsContinents)

		var maxHeight = Math.max.apply(null,populations)
		//console.log(info.get(dias[0]).get(continentes[0]))


		//var names = data.map((d) => { return d.name; }) ;

		var x = d3.scaleBand()
			.domain(continentes)
			.range([0, width])
			.paddingInner(0.2)
			.paddingOuter(0.3);
	
		//var maxHeight = d3.max(data, (d) => { return d.height; });
		console.log(d3.schemeSet3); // list of hex colors
	
		var y = d3.scaleLinear()
			.domain([maxHeight, 0])
			.range([0, height]);
	
		var color = d3.scaleOrdinal()
			.domain(continentes)
			.range(d3.schemeSet3);
	
		var rects = g.selectAll("rect").data(objsContinents);

		rects.enter()
			.append("rect")
				.attr("x", (d) => {
					return x(d.name);
				})
				.attr("y", (d) => {
					return y(d.population);
				})
				.attr("height", (d) => {
					return height - y(d.population);
				})
				.attr("width", x.bandwidth())
				.attr("fill", (d) => {
					return color(d.name);
				})
				.attr("stroke", "black");
	
		// bottom axis ticks
		var bottomAxis = d3.axisBottom(x);
		g.append("g")
		.attr("class", "bottom axis")
		.attr("transform", "translate(0, " + height + ")")
		.call(bottomAxis)
		.selectAll("text")
		.attr("y", "10")
		.attr("x", "-5")
		.attr("text-anchor", "end")
		.attr("transform", "rotate(-20)");
	
		// left y axis
		var yAxisCall = d3.axisLeft(y)
			.ticks(5)
			.tickFormat((d) => { return d ; });
	
		g.append("g")
		.attr("class", "left axis")
		.call(yAxisCall);
		
		// x axis label
		g.append("text")
		.attr("class", "x axis-label")
		.attr("x", (width / 2))
		.attr("y", height + 140)
		.attr("font-size", "20px")
		.attr("text-anchor", "middle")
		.attr("transform", "translate(0, -50)")
		.text("Continents");
	
		// y axis label
		g.append("text")
		.attr("class", "y axis-label")
		.attr("x", - (height / 2))
		.attr("y", -75)
		.attr("font-size", "20px")
		.attr("text-anchor", "middle")
		.attr("transform", "rotate(-90)")
		.text("Population");
	
	}).catch((error)=> {
		console.log(error);

		

	});

	

/*

d3.json("data/buildings.json").then((data)=> {
    
    console.log("Scales");
	data.forEach((d)=>{
		d.height = parseInt(d.height);
	});
    console.log(data);

    var names = data.map((d) => { return d.name; }) ;

    var x = d3.scaleBand()
        .domain(names)
        .range([0, width])
        .paddingInner(0.2)
        .paddingOuter(0.3);

    var maxHeight = d3.max(data, (d) => { return d.height; });
    console.log(d3.schemeSet3); // list of hex colors

    var y = d3.scaleLinear()
        .domain([maxHeight, 0])
        .range([0, height]);

    var color = d3.scaleOrdinal()
        .domain(names)
        .range(d3.schemeSet3);

    var rects = g.selectAll("rect").data(data);
    rects.enter()
        .append("rect")
            .attr("x", (d) => {
                return x(d.name);
            })
            .attr("y", (d) => {
                return y(d.height);;
            })
            .attr("height", (d) => {
                return height - y(d.height);
            })
            .attr("width", x.bandwidth())
            .attr("fill", (d) => {
                return color(d.name);
            })
            .attr("stroke", "black");

    // bottom axis ticks
    var bottomAxis = d3.axisBottom(x);
    g.append("g")
    .attr("class", "bottom axis")
    .attr("transform", "translate(0, " + height + ")")
    .call(bottomAxis)
    .selectAll("text")
    .attr("y", "10")
    .attr("x", "-5")
    .attr("text-anchor", "end")
    .attr("transform", "rotate(-20)");

    // left y axis
    var yAxisCall = d3.axisLeft(y)
        .ticks(5)
	    .tickFormat((d) => { return d + "m"; });

    g.append("g")
    .attr("class", "left axis")
    .call(yAxisCall);
    
    // x axis label
    g.append("text")
    .attr("class", "x axis-label")
    .attr("x", (width / 2))
    .attr("y", height + 140)
    .attr("font-size", "20px")
    .attr("text-anchor", "middle")
    .attr("transform", "translate(0, -50)")
    .text("The word's tallest buildings");

    // y axis label
    g.append("text")
    .attr("class", "y axis-label")
    .attr("x", - (height / 2))
    .attr("y", -60)
    .attr("font-size", "20px")
    .attr("text-anchor", "middle")
    .attr("transform", "rotate(-90)")
    .text("Height (m)");

}).catch((error)=> {
    console.log(error);
});
*/	