create table if not exists motion_detection (
	id int unsigned auto_increment not null,
	detector_name varchar(100) not null,
	detection_time_epoch bigint not null,
	detection_time varchar(50) not null,
	primary key (id),
	index (detection_time_epoch)
);