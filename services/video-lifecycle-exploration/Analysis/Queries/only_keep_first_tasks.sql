WITH row_ranked AS (
	SELECT video_id, prev_schedule_index, scheduled_execution,
    row_number() OVER(PARTITION BY video_id, prev_schedule_index ORDER BY scheduled_execution ASC) as row_num
    from video_scrape_tasks
),
drop_row AS
(
	SELECT video_id, prev_schedule_index, scheduled_execution from row_ranked where row_num > 1
)
delete from video_scrape_tasks vst where exists 
(
	select 1 from drop_row dr where 
		vst.video_id = dr.video_id and 
		vst.prev_schedule_index  = dr.prev_schedule_index and 
		vst.scheduled_execution = dr.scheduled_execution
)


 