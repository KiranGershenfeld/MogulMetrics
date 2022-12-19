import React from 'react';
import axios from 'axios';
import '../css/styles.css'
import * as moment from "moment"

import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';

import { DataGrid } from '@mui/x-data-grid';


function getMonthDay(date)
{
  var d = new Date(date)
  var month = d.getMonth() + 1
  var day = d.getDate()
  return `${month}/${day}`
}

  export default function StreamsTable({data}) {

    data.sort((a,b) => {
      var startDateA = Date.parse(a.start);
      var startDateB = Date.parse(b.start);
      if(startDateA >= startDateB)
      {
        return -1;
      }else
      {
        return 1;
      }
    });

   
    return (
      <div>
      <TableContainer component={Paper}>
        <Table sx={{ minWidth: 650 }} aria-label="simple table">
          <TableHead>
            <TableRow>
              <TableCell align="center">Thumbnail</TableCell>
              <TableCell align="center">Date</TableCell>
              <TableCell align="center">Title</TableCell>
              <TableCell align="center">Hours</TableCell>
              <TableCell align="center">Avg Viewers</TableCell>
              <TableCell align="center">Min Viewers</TableCell>
              <TableCell align="center">Max Viewers</TableCell>

            </TableRow>
          </TableHead>
          <TableBody>
            {data.map((row) => (
              <TableRow
                key={row.title}
                sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
              >
                <TableCell align="center">
                  <a href={`https://youtube.com/watch?v=${row.video_id}`}><img className='table-thumbnail' src={row.thumbnail_url} /></a>
                </TableCell>
                <TableCell align="center">{getMonthDay(row.start)}</TableCell>
                <TableCell align="center">{row.title}</TableCell>
                <TableCell align="center">{row.hours.toFixed(2)}</TableCell>
                <TableCell align="center">{row.avg_viewers.toFixed(0)}</TableCell>
                <TableCell align="center">{row.min_viewers}</TableCell>
                <TableCell align="center">{row.max_viewers}</TableCell>

              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
      </div>

    );
  }