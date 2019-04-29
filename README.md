Redis
=========

Redis role, which can be used to create variety of Redis setups:
* single node
* single master node with multiple replicas
* Redis cluster

Majoriy of work is based on already existing role: [DavidWittman.redis](https://galaxy.ansible.com/davidwittman/redis)

To-do list
-------
* automate Cluster deployment mode
* add Sentinel configuration

Installation
------------

`ansible-galaxy install BostjanBozic.redis`

Getting started
------------

Role is used to create variety of Redis setups. Role has to be run with sudo rights on remote machines.

### Single Redis Node

Deploying single Redis node requires usage of this role, without any variable modifications needed. This is example of playbook with specified port on which Redis will run:
```
---

- hosts: all
  roles:
    - BostjanBozic.redis
  vars:
    - redis_port: 6380
```

After playbook and inventory files are specified (e.g. `playbook.yml` and `inventory`), you deploy Redis with following command:

`ansible-playbook -i inventory playbook.yml`

### Single Master Node with Replication

Redis supports replication setup, where single master node is backed by single or multiple replication nodes. Example below deploys single Redis master instance with 2 replicas:

Inventory file:
```
[master]
redis-master-0.example.io

[replica]
redis-replica-0.example.io master_host=redis-master-0.example.io
redis-replica-1.example.io master_host=redis-master-0.example.io
```

Playbook file:
```
---

- hosts: master
  roles:
    - BostjanBozic.redis

- hosts: replica
  roles:
    - BostjanBozic.redis
  vars:
    - replicaof: {{ master_host }} {{ redis_port }}  
```

**Note**: replication and cluster node are mutually exclusive. When using `replicaof` variable, do not set up `redis_cluster_enabled` variable.

### Cluster mode (EXAMPLE WORK IN PROGRESS)

Redis also supports cluster mode, where data is distributed over multiple master nodes, which can be backed by one or more replication nodes. Example below deploys 3 Redis master instances with 1 replication node each:

Inventory file:
```
[master]
redis-master-[0:2].example.ui

[replica]
redis-replica-0.example.io master_host=redis-master-0.example.io
redis-replica-1.example.io master_host=redis-master-1.example.io
redis-replica-2.example.io master_host=redis-master-2.example.io
```

Playbook file:
```
---

- hosts: all
  roles:
    - BostjanBozic.redis
  vars:
    - redis_cluster_enabled: "yes"

- hosts: master
  command: redis-cli --cluster create {{ master_ip:port }}
  
- hosts: replica
  command: redis-cli --cluster add-node {{ replica_ip:port }} {{master_ip:port }} --cluster-slave
```

**Note**: replication and cluster node are mutually exclusive. When using `redis_cluster_enabled` variable, do not set up `replicaof` variable.


Role Variables
--------------

This is list of default variables. For description, please check [official documentation](http://download.redis.io/redis-stable/redis.conf).

```
---

## Installation
redis_version: 5.0.4
redis_install_dir: /opt/redis
redis_download_url: "http://download.redis.io/releases/redis-{{ redis_version }}.tar.gz"

redis_user: redis
redis_group: redis

redis_nofile_limit: 16384
redis_oom_score_adjust: 0

## Redis Serivce
redis_as_service: true
redis_service_name: "redis_{{ redis_port }}"

## Redif config
# Network options
redis_bind: 0.0.0.0
redis_protected_mode: "no"
redis_port: 6379
redis_tcp_backlog: 511
redis_timeout: 0
redis_tcp_keepalive: 300

# General configuration
redis_daemonize: "yes"
redis_supervised: "no"
redis_pidfile: /var/run/redis/{{ redis_port }}.pid
redis_loglevel: notice
redis_logfile: /var/log/redis_{{ redis_port }}.log
redis_databases: 16

# Snapshotting configuration
redis_save:
  - 900 1
  - 300 10
  - 60 10000
redis_stop_writes_on_bgsave_error: "yes"
redis_rdbcompression: "yes"
redis_rdbchecksum: "yes"
redis_dbfilename: dump.rdb
redis_dir: /var/lib/redis/{{ redis_port }}

# Replication configuration
redis_replicaof: false
redis_replica_serve_stale_data: "yes"
redis_replica_read_only: "yes"
redis_repl_diskless_sync: "no"
redis_repl_diskless_sync_delay: 5
redis_repl_disable_tcp_nodelay: "no"
redis_repl_backlog_size: false
redis_replica_priority: 100
redis_min_replicas_to_write: 0
redis_min_replicas_max_lag: 10

# Security configuration
redis_password: false

# Clients configuration
redis_maxclients: 10000

# Memory Management configuration
redis_maxmemory: false
redis_maxmemory_policy: noeviction

# Lazy Freeing configuration
redis_lazyfree_lazy_eviction: "no"
redis_lazyfree_lazy_expire: "no"
redis_lazyfree_lazy_server_del: "no"
redis_replica_lazy_flush: "no"

# Append Only Mode configuration
redis_appendonly: "no"
redis_appendfilename: "appendonly.aof"
redis_appendfsync: everysec
redis_no_appendfsync_on_rewrite: "no"
redis_auto_aof_rewrite_percentage: 100
redis_auto_aof_rewrite_min_size: 64mb
redis_aof_load_truncated: "yes"

# Lua Scripting configuration
redis_lua_time_limit: 5000

# Redis Cluster configuration
redis_cluster_enabled: "no"
redis_cluster_config_file: nodes-{{ redis_port }}.conf
redis_cluster_node_timeout: 15000

# Slow Log configuration
redis_slowlog_log_slower_than: 10000
redis_slowlog_max_len: 128

# Latency Monitor configuration
redis_latency_monitor_threshold: 0

# Event Notification configuration
redis_notify_keyspace_events: '""'

# Advanced Config configuration
redis_client_output_buffer_limit_normal: 0 0 0
redis_client_output_buffer_limit_replica: 256mb 64mb 60
redis_client_output_buffer_limit_pubsub: 32mb 8mb 60
```

License
-------

This project is licenced under [MIT](https://opensource.org/licenses/MIT) licence
