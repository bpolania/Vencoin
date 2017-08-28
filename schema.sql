drop table if exists pareto;
create table pareto (
  id integer primary key autoincrement,
  time timestamp default (strftime('%s', 'now')),
  'value' text not null
);

drop table if exists top;
create table top (
  id integer primary key autoincrement,
  time timestamp default (strftime('%s', 'now')),
  'value' text not null
);
