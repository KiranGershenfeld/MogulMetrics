import React from 'react';
import { useState } from 'react';

import axios from 'axios';
import * as d3 from "d3";
import * as d3_chromatic from "d3-scale-chromatic"
import '../css/styles.css'
import * as moment from "moment"

function getFirstDayOfMonth(month, year){
}

function daysInMonth (month, year) {
}

const VideoViewPlot = ({ data, dimensions }) => {

    console.log("Drawing video view plot")

    const [idTitleMapping, setIdTitleMapping] = useState([])

    const svgRef = React.useRef(null);
    var colorScale = null;
    var { width, height, margin } = dimensions;
    var legend_width = 0
    var svgWidth = width + margin.left + margin.right;
    var svgHeight = height + margin.top + margin.bottom;

    React.useEffect(() => {
        width = document.getElementById("video-chart-container").offsetWidth
        svgWidth = width + margin.left + margin.right;
        var plot_width = width - legend_width

        if(data.length == 0)
        {
            return
        }
        let video_ids = []
        let time_deltas = []
        let view_counts = []
        let dates_of_upload = []
        let video_titles = []

        data.map((e) => {
            video_ids.push(e["video_id"]);
            time_deltas.push(e["time_delta"]);
            view_counts.push(e["views"]);
            dates_of_upload.push(e["date_uploaded"])
            video_titles.push(e["video_title"]);
        })

        const svgEl = d3.select(svgRef.current);
        svgEl.selectAll("*").remove(); // Clear svg content before adding new elements 
        const svg = svgEl
            .attr("width", width)
            .attr("height", height)
            .append("g")
            .attr("transform", `translate(${margin.left},${margin.top})`);

        var x = d3.scaleLinear()
            .domain(d3.extent(time_deltas))
            .range([ 0, plot_width]);

        svg.append("g")
            .attr("transform", "translate(0," + (height - margin.bottom) + ")")
            .call(d3.axisBottom(x).ticks(20));

        svg.append("text")
            .attr("class", "x label")
            .attr("text-anchor", "end")
            .attr("x", (width / 2) - 10)
            .attr("y", height - 10)
            .style("font-size", "0.8em")
            .text("Hours past upload");
        
          // Add Y axis
          var y = d3.scaleLinear()
            .domain(d3.extent(view_counts))
            .range([ height - margin.bottom, 0]);
          svg.append("g")
            .call(d3.axisLeft(y));

        svg.append("text")
            .attr("class", "y label")
            .attr("transform", "rotate(-90)")
            .attr("dy", ".75em")
            .attr("x", -(height / 2))
            .attr("y", - margin.left)
            .style("font-size", "0.8em")
            .text("View Count");

        colorScale = d3.scaleOrdinal(d3.schemeCategory10)
            .domain(new Set(video_ids))

        var unique_vid_ids = new Set(video_ids)
        var ids_titles_mapping = []
        unique_vid_ids.forEach((value) => {
            ids_titles_mapping.push({
                "video_id": value, 
                "video_title": video_titles[video_ids.lastIndexOf(value)],
                "color": colorScale(value)
            })
        })
        setIdTitleMapping(ids_titles_mapping)

          // Add dots
        svg.append('g')
            .selectAll("dot")
            .data(data)
            .enter()
            .append("circle")
              .attr("cx", function (d) { return x(d.time_delta); } )
              .attr("cy", function (d) { return y(d.views); } )
              .attr("r", 2)
              .style("fill", function (d) {return colorScale(d.video_id); })


        // svg.append('g')
        //     .selectAll("legend-dot")
        //     .data(new Set(video_ids))
        //     .enter()
        //     .append("circle")
        //         .attr("cx", plot_width + 30)
        //         .attr("cy", function(d,i){ return 100 +  i*25}) // 100 is where the first dot appears. 25 is the distance between dots
        //         .attr("r", 4)
        //         .style("fill", function(d){ return "blue"})

        // svg.append("g")
        //     .selectAll("legend-label")
        //     .data(new Set(video_ids))
        //     .enter()
        //     .append("text")
        //         .attr("x", plot_width + 45)
        //         .attr("y", function(d,i){ return 100 + i*25}) // 100 is where the first dot appears. 25 is the distance between dots
        //         .style("fill", function(d){ return "black"})
        //         .text(function(d){ return "SAMPLE TITLE WITH SPACES"})
        //         .attr("text-anchor", "left")
        //         .style("alignment-baseline", "middle")
      }, [data]);

    return (<div>
            <svg ref={svgRef} width={svgWidth} height={svgHeight}/>
            <div style={{marginTop: "20px", marginBottom: "50px"}}>
                    { // black magic dont delete
                    } 
                    {(idTitleMapping.map(function(d, idx){
                        
                        return (
                            <div style={{display: "flex"}}>
                                <div style={{
                                        content: "\u2B24",
                                        fontWeight: "bold", 
                                        display: "inline-block",
                                        width: "3em",
                                        marginTop: "0.8em",
                                        fontSize: "0.5em",
                                        color: d.color
                                }}>
                                    {'\u2B24'}
                                </div>

                                <div >
                                    {<a href={`https://youtube.com/watch?v=${d.video_id}`} target="_blank">{d.video_title}</a>}
                                </div>
                            </div>
                        )  
                    }))
                    }
            </div>
        </div>);
}

export default VideoViewPlot;
