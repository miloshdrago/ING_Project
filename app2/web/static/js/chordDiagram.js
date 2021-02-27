

function d3ChordDiagram(endpoint_matrix) {

    // If endpoint_matrix contained data, return D3 visualization
    if (endpoint_matrix['message'] == 'Success') {
        
          // create the svg area
          var svg = d3.select("#my_dataviz")
            .append("svg")
              .attr("width", 500)
              .attr("height", 500)
            .append("g")
              .attr("transform", "translate(250,250)")

          // create a matrix
          var matrix = endpoint_matrix['data']['matrix'];
          var names = endpoint_matrix['data']['names'];

          // give this matrix to d3.chord(): it will calculates all the info we need to draw arc and ribbon
          var res = d3.chord()
              .padAngle(0.05)
              .sortSubgroups(d3.descending)
              (matrix)

          // add the groups on the inner part of the circle
          svg
            .datum(res)
            .append("g")
            .selectAll("g")
            .data(function(d) { return d.groups; })
            .enter()
            .append("g")
            .append("path")
              .style("fill", "#ff6200")
              .style("stroke", "black")
              .attr("d", d3.arc()
                .innerRadius(230)
                .outerRadius(240)
              )

          // Add a tooltip div. Here I define the general feature of the tooltip: stuff that do not depend on the data point.
          // Its opacity is set to 0: we don't see it by default.
          var tooltip = d3.select("#my_dataviz")
            .append("div")
            .style("opacity", 0)
            .attr("class", "tooltip")
            .style("background-color", "white")
            .style("border", "solid")
            .style("border-width", "1px")
            .style("border-radius", "5px")
            .style("padding", "1px")
            .style("position", "absolute")
            .style("left", "-300px")
            .style("top", "30px")


          // A function that change this tooltip when the user hover a point.
          // Its opacity is set to 1: we can now see it. Plus it set the text and position of tooltip depending on the datapoint (d)
          var showTooltip = function(d) {
            tooltip
              .style("opacity", 1)
              .html("Source: " + names[d.source.index] + "<br>Target: " + names[d.target.index])
              .style("left", (d3.event.pageX + 15) + "px")
              .style("top", (d3.event.pageY - 28) + "px")
          }

          // A function that change this tooltip when the leaves a point: just need to set opacity to 0 again
          var hideTooltip = function(d) {
            tooltip
              .transition()
              .duration(1000000000)
              .style("opacity", 0)
          }

          // Add the links between groups
          svg
            .datum(res)
            .append("g")
            .selectAll("path")
            .data(function(d) { return d; })
            .enter()
            .append("path")
              .attr("d", d3.ribbon()
                .radius(220)
              )
              .style("fill", "#c3bfb7")
              .style("stroke", "black")
            .on("mouseover", showTooltip )
            .on("mouseleave", hideTooltip )


        
  }

  // Else, show logfile not found error message 
  else {
      var failure_message = "No logfile found to generate visualization. A simulation must be run first."
      
      document.getElementById('my_dataviz').innerHTML = failure_message;
      console.log(failure_message)

  }
}