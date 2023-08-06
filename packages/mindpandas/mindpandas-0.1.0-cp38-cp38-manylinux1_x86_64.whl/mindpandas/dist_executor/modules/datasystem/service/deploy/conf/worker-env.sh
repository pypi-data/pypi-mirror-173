#!/bin/bash
# Copyright (c) 2022 Huawei Technologies Co., Ltd.
#
# This software is licensed under Mulan PSL v2.
# You can use this software according to the terms and conditions of the Mulan PSL v2.
# You may obtain a copy of Mulan PSL v2 at:
#
# http://license.coscl.org.cn/MulanPSL2
#
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND,
# EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT,
# MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
# See the Mulan PSL v2 for more details.
#
# Edit this file to configure startup parameters, it is sourced to launch components.

# Address of worker and the value cannot be empty. (Default: "127.0.0.1:9088")
# WORKER_ADDRESS="127.0.0.1:9088"

# Address of master and the value cannot be empty. (Default: "127.0.0.1:9089")
# WORKER_MASTER_ADDRESS="127.0.0.1:9089"

# Upper limit of the shared memory, the unit is mb, must be greater than 0. (Default: "64")
# WORKER_SHARED_MEMORY_SIZE_MB="64"

# Time interval between worker and master heartbeats. (Default: "1000")
# WORKER_HEARTBEAT_INTERVAL_MS="1000"

# Indicates whether to enable the tenant authentication, default is false. (Default: "false")
# WORKER_AUTHORIZATION_ENABLE="false"

# Enable unix domain socket. (Default: "true")
# WORKER_ENABLE_UDS="true"

# The number of regular backend socket for stream cache (Default: "32")
# WORKER_SC_REGULAR_SOCKET_NUM="32"

# The number of stream backend socket for stream cache. (Default: "32")
# WORKER_SC_STREAM_SOCKET_NUM="32"

# Size of the page used for caching worker files. The valid range is 4096-1073741824. (Default: "1048576")
# WORKER_PAGE_SIZE="1048576"

# The max size of the stream allowed to use on this worker. (Default: "1024")
# WORKER_MAX_STREAM_SIZE_MB="1024"

# The num of threads used to send elements to remote worker. (Default: "8")
# WORKER_REMOTE_SEND_THREAD_NUM="8"

# The sleep microseconds after scan remote send task. (Default: "10")
# WORKER_SCAN_REMOTE_SEND_INTERVALS_US="10"

# The redis IP address host:port. If the redis service is required, the address must be set. ex: 127.0.0.1:6379 (Default: "")
# WORKER_REDIS_ADDRESS=""

# The path and file name prefix of the spilling, empty means spill disabled. (Default: "")
# WORKER_SPILL_DIRECTORIES=""

# The size limit of spilled data, 0 means unlimited. (Default: "0")
# WORKER_SPILL_SIZE_LIMIT="0"

# The redis username for auth. (Default: "")
# WORKER_REDIS_USERNAME=""

# The redis password for auth. (Default: "")
# WORKER_REDIS_PASSWD=""

# Config rpc server thread number, must be greater than 0. (Default: "16")
# WORKER_RPC_THREAD_NUM="16"

# The directory to store unix domain socket file. The UDS generates temporary files in this path. (Default: "~/.datasystem/unix_domain_socket_dir")
# WORKER_UNIX_DOMAIN_SOCKET_DIR="~/.datasystem/unix_domain_socket_dir"

# The directory where log files are stored. (Default: "~/.datasystem/logs")
# WORKER_LOG_DIR="~/.datasystem/logs"

# Maximum log file size (in MB), must be greater than 0. (Default: "512")
# WORKER_MAX_LOG_SIZE="512"

# All log files max size (in MB), must be greater than 'MASTER_MAX_LOG_SIZE'. Log will roll if the size is exceeded. (Default: "10000")
# WORKER_TOTAL_LOG_SIZE_MB="10000"

# Flush log files with async mode. (Default: "false")
# WORKER_LOG_ASYNC="false"

# Compress old log files in .gz format. This parameter takes effect only when the size of the generated log is greater than max log size. (Default: "true")
# WORKER_LOG_COMPRESS="true"

# vlog level. (Default: "0")
# WORKER_V="0"

# Enable zmq authentication (Default: "false")
# WORKER_ZMQ_ENABLE_AUTH="false"

# The directory to find ZMQ curve key files. This path must be specified when zmq authentication is enabled. (Default: "")
# WORKER_CURVE_KEY_DIR=""
