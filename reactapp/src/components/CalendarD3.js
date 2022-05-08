import React from 'react';
import axios from 'axios';
import * as d3 from "d3";
import * as d3_chromatic from "d3-scale-chromatic"
import '../css/styles.css'
import * as moment from "moment"

/*
This component must take in a list of objects each of which contains a date and a value for hours streamed, the month to draw, and the dimensions of the desired calendar.
NOTE* There is a disconnect between the dates of the data given and which month is being drawn. For instance if the data contains only days from february and a few from august
what month should the calendar draw. In order for the result to make sense *most* of the time I will set it up to draw the month given as a parameter and look for dates within 
that month range. The calendar will then draw the month with any valid dates given (hopefully all matching) greying out dates that have not occured yet. 
*/
function getFirstDayOfMonth(month, year){
  return moment(year + "-" + month + "-01T00:00:00.000Z")
}

function daysInMonth (month, year) {
  return new Date(year, month, 0).getDate();
}

const CalendarD3 = ({ data, month, year, dimensions }) => {
    console.log("Calling Calendar")

    const svgRef = React.useRef(null);
    var { width, height, margin } = dimensions;
    const svgWidth = width + margin.left + margin.right;
    const svgHeight = height + margin.top + margin.bottom;

    const day_cols = {"Sunday": 0, "Monday": 1, "Tuesday": 2, "Wednesday": 3, "Thursday": 4, "Friday": 5,"Saturday": 6}
    const days= ["M", "M", "T", "W", "Th", "F", "S"]

    const first_day = getFirstDayOfMonth(month, year)
    const number_days_in_month = daysInMonth(month, year)
    const days_per_row = 7
    const grid_margin = 10
    const cellSize = ((width - (6* grid_margin)) / 7) - 1
    // const formatDay = d => ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"][d.getUTCDay()]
    // const countDay = d => d.getUTCDay()
    const timeWeek = d3.utcSunday

    //Create data for calendar, this array must be the number of days in the specified month. Objects in this array are tagged with a "valid" key to determine if data was actually specified for that date.
    var calendar_data = []
    var date_iterator = first_day
    var data_index = 0
    var max_hours_streamed = 0
    var label_height_offset = 20

    var first_day_offset = (first_day.day() + 1) % 7

    for(var i = 0; i < number_days_in_month + first_day_offset; i++)
    {
      var day_obj = {}
      var column_index = i % days_per_row
      var row_index = Math.floor(i / days_per_row)

      day_obj["x"] = column_index * (cellSize + grid_margin)
      day_obj["y"] = row_index * (cellSize + grid_margin) + label_height_offset

      if(i < first_day_offset)
      {
        day_obj["in_month"] = false
        calendar_data.push(day_obj)
      }else
      {
        day_obj["in_month"] = true

        if(data_index < data.length && data[data_index]["date"].isSame(date_iterator, "day"))
        {
          day_obj["valid"] = true
          day_obj["date"] = data[data_index]["date"]
          day_obj["streamed_hours"] = data[data_index]["streamed_hours"]
          if(day_obj["streamed_hours"] > max_hours_streamed)
          {
            max_hours_streamed = day_obj["streamed_hours"]
          }

          data_index++
          
        }else
        {
          day_obj["valid"] = false
          day_obj["date"] = date_iterator
          day_obj["streamed_hours"] = 0
        }

        calendar_data.push(day_obj)

        date_iterator = date_iterator.add("1", "days")

      }

      
    }

    var label_data = []
    for(var i = 0; i < 7; i++)
    {
      var column_index = i % days_per_row
      
      var label_obj = {}
      label_obj["text"] = days[i]
      label_obj["x"] = column_index * (cellSize + grid_margin) + (cellSize/2)
      label_obj["y"] = 10
      label_data.push(label_obj)
    }


    React.useEffect(() => {


      const svgEl = d3.select(svgRef.current);
      svgEl.selectAll("*").remove(); // Clear svg content before adding new elements 
      const svg = svgEl
        .attr("width", width)
        .attr("height", height)
        .append("g")
         .attr("transform", `translate(${margin.left},${margin.top})`);

      const colorScale = d3.scaleSequential(d3_chromatic.interpolateGreens)
        .domain([0, max_hours_streamed + 2])

      console.log(label_data)
      //Creating row labels
      svg.selectAll(".column_label")
        .data(label_data)
        .enter()
          .append("text")
            .attr("x", (d) => d.x)
            .attr("y", (d) => d.y)
            .text(function(d)
            {
              return d["text"]
            })
            .style("text-anchor", "middle")
      //Creating a grid of objects in d3
      svg.selectAll(".day")
        .data(calendar_data)
        .enter()
          .append("rect")
          .attr("width", cellSize)
          .attr("height", cellSize)
          .attr("x", (d) => d.x)
          .attr("y", (d) => d.y)
          .attr("fill", function(d){
            if(d.valid){return colorScale(d["streamed_hours"])}
            else{return "#ebebeb"}
          })
    }, [data]);
  
    return <svg ref={svgRef} width={svgWidth} height={svgHeight} />;
  
}

export default CalendarD3;