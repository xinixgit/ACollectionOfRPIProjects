with t as (select min(id) as min_id from motion_detection),
curr as (select id, detection_time_epoch as ts from motion_detection, t where id > t.min_id),
prev as (select (id + 1) as id, detection_time_epoch as ts from motion_detection)

select
	round(avg(x.elapsed_min), 2) as avg,
	round(max(x.elapsed_min), 2) as max,
	round(min(x.elapsed_min), 2) as min
from
(
select
	(c.ts - p.ts) / 60 as elapsed_min
from curr c, prev p
where c.id = p.id
) x
;