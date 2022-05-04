import React from 'react';
import axios from 'axios';
import * as d3 from "d3";
import '../css/styles.css'


const CalendarD3 = ({ data, dimensions }) => {

    const svgRef = React.useRef(null);
    const { width, height, margin } = dimensions;
    const svgWidth = width + margin.left + margin.right;
    const svgHeight = height + margin.top + margin.bottom;

    const cellSize = 15
    const yearHeight = cellSize * 7 + 25
    const formatDay = d => ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"][d.getUTCDay()]
    const countDay = d => d.getUTCDay()
    const timeWeek = d3.utcSunday

    React.useEffect(() => {
      console.log("React use effect")
      const x = d3.scaleLinear()
        .domain([0, 10])
        .range([0, width])
      const y = d3.scaleLinear()
        .domain([0, 10])
        .range([height, 0])
      
      const svgEl = d3.select(svgRef.current);
      svgEl.selectAll("*").remove();

      const svg = svgEl
        .append("g")
        .attr("transform", `translate(${margin.left},${margin.top})`);

      const xAxis = d3.axisBottom(x)
        .ticks(5)
        
      svg.append('g').call(xAxis);

      const yAxis = d3.axisLeft(y)
        .ticks(5)

      svg.append('g').call(yAxis);

      svg.selectAll(".dot")
        .data(data)
        .enter()
          .append("circle")
          .attr("fill", "black")
          .attr("r", 4)
          .attr("cx", (d)=> x(d.x))
          .attr("cy", (d)=> x(d.y))

    }, [data]);
  
    return <svg ref={svgRef} width={svgWidth} height={svgHeight} />;
  
}

export default CalendarD3;