delete 
from video_scrape_tasks 
where video_scrape_tasks.video_id in (
	select video_scrape_tasks.video_id 
	from video_scrape_tasks 
	join video_notification_feed 
		on video_scrape_tasks.video_id = video_notification_feed.video_id 
	where video_notification_feed.channel_id in 
	('UCLXo7UDZvByw2ixzpQCufnA',
	'UCupvZG-5ko_eiXAupbDfxWw',
	'UCXIJgqnII2ZOINSWNOGFThA',
	'UCNbIDJNNgaRrXOD7VllIMRQ',
	'UCaXkIU1QidjPwiAYu6GcHjg',
	'UCmgnsaQIK1IR808Ebde-ssA',
	'UCtUbO6rBht0daVIOGML3c8w',
	'UCNvsIonJdJ5E4EXMa65VYpA',
	'UClt01z1wHHT7c5lKcU8pxRQ',
	'UCmh5gdwCx6lN7gEC20leNVA')
	and video_scrape_tasks.task_status = 'Scheduled'
)
and video_scrape_tasks.task_status = 'Scheduled'