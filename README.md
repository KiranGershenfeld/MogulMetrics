# MogulMetrics
Welcome to MogulMetrics, a dashboard of aggregated metrics for all Mogul Moves social meida outlets. This tool is designed from the ground up for the YouTube livestreaming ecosystem and aims to fill the gaps in YouTube's live stream analytics.

Currently hosted at [mogulmetrics.net](https://www.mogulmetrics.net)

The project is still in its infancy and is not yet hosted anywhere. No planned metrics or views require proprietary channel information so MogulMetrics will launch accessible to the general public.

## Roadmap
This is a rough outline of ideas for what will be included in the dashboard:

* Daily hours streamed for a given week with totals and averages
     * Ludwig's channel will be pinged every 10 minutes
     * This log will then be fed into a weekly bar chart

* Combined metrics topline metrics for all 5 channels
     * Top channels that week/month
     * Best performing recent videos across all channels
     * Net change in subscribers across all channels

* Full social media dashboard including Twitter, Discord, Instagram, etc. This allows growth to be tracked holistically for the MogulMoves brand

## Contribution
This is a fairly modular project which lends to easy contributions from the community. If there are statistics and metrics that you think would be useful to the MogulMoves team please reach out! If you have the skills to contribute to the development process, let me know and we can talk about access to databases and such.

## Tech Stack
This project is build with PostgreSQL, Django, React.js, and D3.js
The database is currently hosted by CoackroachDB as it has a generous free tier for PostgreSQL.
The scheduled scripting is running on AWS Lambda and EC2 instances. 

If you are familiar with these tools and passionate about social media data science contributions are always welcome.   
