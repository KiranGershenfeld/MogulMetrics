import React from 'react';
import { useState } from 'react';

import '../css/styles.css'
import MogulNavBar from './Navbar'

const AboutPage = () => {
    return (
        <div>
            <MogulNavBar />
            <div style={{margin: "auto", marginTop: "25px", width: "40%", textAlign:"center"}}>
                <div>
                    <span className='about-heading'>About</span>
                    <div className='about-spacer-small'></div>
                    This website is a visual dashboard Mogul Moves related metrics
                    <div className='about-spacer'></div>
                    The livestream calendar and streams table are built by checking YouTube every 10 minutes via a combination of API calls and webscraping. The video lifecycle page listens for uploaded videos and checks their viewcounts over time, showing how the algorithm is recommending content.   
                    <div className='about-spacer'></div>
                    Mogul Metrics is an <a href='https://github.com/KiranGershenfeld/MogulMetrics' target='_blank'>open source</a> project mainly built by <a href='https://www.linkedin.com/in/kirangershenfeld/' target='_blank'> me, Kiran</a>. Check out my other projects including the popular <a href='https://www.reddit.com/r/LivestreamFail/comments/mu8nyp/twitch_atlas_vol_3/' target='_blank'>Twitch</a> and <a href='https://youtubeatlas.com' target='_blank'>YouTube</a> Atlas maps on my <a href="https://github.com/KiranGershenfeld">Github</a>! Sorry for any usability issues, web development is not my strong suit. 
                    <div className='about-spacer'></div>
                    In general I think understanding data can help content creators grow and understand their audience. This dashboard, alongside my other projects, aims to increase that understanding. 
                    <div className='about-spacer'></div>
                    If you'd like to contribute or talk about these projects please reach out!
                    Contact me at <a href='mailto:kiran@gershenfeld.org' target='_blank'>kiran@gershenfeld.org</a> with any inquiries, questions, requests, or concerns
                    <div className='about-spacer'></div>
                    <div className='about-spacer'></div>
                    <span className='about-heading'>Tech Stack</span>
                    <div className='about-spacer-small'></div>
                    <span className='about-heading-small'>Backend</span>
                    <div className='about-spacer-small'></div>
                    The backend for this dashboard is built as a Django REST API written in python and hosted on an EC2 instance. The database uses PostgreSQL on CockroachDB as they provide a generous free tier (cloud hosted on AWS). 
                    <div className='about-spacer'></div>
                    The data for the livestreams page is collected with an AWS Lambda function that runs every 10 minutes. This function uses webscraping to check if the channel is live and if so uses the YouTube API to collect information about the stream. This two step process is done to save on quota usage for the API. The video lifecycle data is retrieved on a seperate EC2 instance that is hosting a flask server subscribed to several youtube channels via PubSubHubub. When a new video is published a series of tasks begins to query that video for views according to a predefined schedule.
                    <div className='about-spacer'></div>
                    <span className='about-heading-small'>Frontend</span>
                    <div className='about-spacer-small'></div>
                    The frontend is built in React.js and deployed using Netlify. The graphs are created in D3.js. The styling is a real blend of mui, basic css, and whatever pre-built elements I could find. I'm very much still learning frontend so its not the prettiest but a webapp felt like the best solution (Unless someone wants to shell out for a Tableau license)





                    <div className='about-spacer'></div>

                </div>
            </div>
        </div>);
}

export default AboutPage;
