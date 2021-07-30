USE exports;

SELECT DISTINCT substring(`t_created`, 1, 10) AS `date_created` FROM `gps_loc`;


SELECT
	AVG(`lat`) as `lat`
	, AVG(`lng`) as `lng`
	, FLOOR(AVG(`ts_epoch`)) as `ts_epoch`
INTO OUTFILE '/home/pi/exported_data/gps_loc.csv'
FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n'
FROM gps_loc
WHERE `t_created` LIKE '7/23/2021%'
GROUP BY substring(`t_created`, 1, 17)
ORDER BY `ts_epoch` ASC
;

SELECT COUNT(*) FROM
(
SELECT
	AVG(`lat`) AS `lat`
FROM gps_loc
WHERE `t_created` LIKE '7/23/2021%'
GROUP BY substring(`t_created`, 1, 17)
ORDER BY `ts_epoch` ASC
) x
;