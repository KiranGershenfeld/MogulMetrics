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
                    The data here is collected with in-house scrapes and databases, without reliance on the YouTube API. The video view data shown on the <a href="/videolifecycle" target='_blank'>Video View Lifecycle</a> page provides a window into how videos are recommended and viewed over time. 
                    <br></br>
                    <br></br>
                    Mogul Metrics is an <a href='https://github.com/KiranGershenfeld/MogulMetrics' target='_blank'>open source</a> project mainly built by <a href='https://www.linkedin.com/in/kirangershenfeld/' target='_blank'>Kiran Gershenfeld</a>. Check out my other projects including the popular <a href='https://www.reddit.com/r/LivestreamFail/comments/mu8nyp/twitch_atlas_vol_3/' target='_blank'>Twitch</a> and <a href='https://youtubeatlas.com' target='_blank'>YouTube</a> Atlas maps on my <a href="https://github.com/KiranGershenfeld">Github</a>! Sorry for any usability issues, web development is not my strong suit.  
                    <br></br>
                    <br></br>
                    <b>The world of content creation is regulated by data driven algorithms and understanding this data can be a tool for consistent growth across platforms.</b>
                    <br></br>
                    <br></br>
                    Contact me at <a href='mailto:kiran@gershenfeld.org' target='_blank'>kiran@gershenfeld.org</a> with any inquiries, questions, requests, or concerns
                </div>
            </div>
        </div>);
}

export default AboutPage;
