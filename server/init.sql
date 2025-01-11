-- auto-generated definition
create table sys_server_monitor
(
    id           bigint               not null
        primary key,
    server_name  varchar(64)          not null comment '服务器名称',
    ip           varchar(64)          not null comment '服务器ip',
    url          varchar(128)         null comment '监控地址',
    enable       tinyint(1) default 1 null comment '是否启用 1启用，0停用',
    update_time  datetime             null comment '修改时间',
    cpu_percent  decimal(10, 3)       null comment 'CPU百分比',
    mem_used     decimal(10, 3)       null comment '内存使用大小G',
    mem_free     decimal(10, 3)       null comment '内存剩余大小G',
    mem_total    decimal(10, 3)       null comment '内存总大小G',
    mem_percent  decimal(10, 3)       null comment '内存使用率%',
    disk_used    decimal(10, 3)       null comment '硬盘使用大小G',
    disk_free    decimal(10, 3)       null comment '硬盘剩余大小G',
    disk_total   decimal(10, 3)       null comment '硬盘总大小G',
    disk_percent decimal(10, 3)       null comment '硬盘使用率%'
)
    comment '服务器情况监控' engine = InnoDB;

insert into sys_server_monitor(id, server_name, ip, url, enable)
    value (1, '测试服务器', '127.0.0.1', 'http://127.0.0.1:8090/monitor', 1)
