create table if not exists gps_loc (
	id int unsigned auto_increment not null,
	lat varchar(100) not null,
	lng varchar(100) not null,
	ts_epoch bigint not null,
	t_created varchar(100) not null,
	alt varchar(100),
	geoidal varchar(100),
	valid varchar(100),
	primary key (id),
	index (t_created)
);