import React from 'react';
import { useState } from 'react';

import '../css/styles.css'
import MogulNavBar from './Navbar'

const AboutPage = () => {
    return (
        <div>
            <MogulNavBar />
            <div style={{margin: "auto", marginTop: "25px", width: "40%", textAlign:"center"}}>
                <div>This website is a visual dashboard Mogul Moves related metrics
                    <br></br>
                    <br></br>
                    The data here is collected with in-house scrapes and databases, without reliance on the YouTube API. The granular video view data shown on the <a href="/videolifecycle" target='_blank'>Video View Lifecycle</a> page delivers novel insights into how videos are recommended and viewed over time. 
                    <br></br>
                    <br></br>
                    Mogul Metrics is an <a href='https://github.com/KiranGershenfeld/MogulMetrics' target='_blank'>open source</a> project mainly built by <a href='https://www.linkedin.com/in/kirangershenfeld/' target='_blank'>Kiran Gershenfeld</a>. I am also the creator of the <a href='https://www.reddit.com/r/LivestreamFail/comments/mu8nyp/twitch_atlas_vol_3/' target='_blank'>Twitch</a> and <a href='https://youtubeatlas.com' target='_blank'>YouTube</a> atlas maps that became popular in online communities about  a year ago. I am a data scientist/data engineer by trade, not a web designer, so please forgive any formatting or usability quirks. 
                    <br></br>
                    <br></br>
                    <b>The world of content creation is regulated by data driven algorithms and I believe that understanding this data can be a tool for consistent growth accross platforms.</b>
                    <br></br>
                    <br></br>
                    Contact me at <a href='mailto:kiran@gershenfeld.org' target='_blank'>kiran@gershenfeld.org</a> with any inquiries, questions, requests, or concerns
                </div>
            </div>
        </div>);
}

export default AboutPage;
