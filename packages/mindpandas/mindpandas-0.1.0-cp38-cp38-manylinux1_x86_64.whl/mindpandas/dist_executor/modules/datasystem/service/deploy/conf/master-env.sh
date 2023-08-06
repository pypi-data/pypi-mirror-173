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

# Address of master and the value cannot be empty. (Default: "127.0.0.1:9089")
# MASTER_ADDRESS="127.0.0.1:9089"

# Config MASTER back store directory and must specify in rocksdb scenario. The rocksdb database is used to persistently store the metadata stored in the master so that the metadata before the restart can be re-obtained when the master restarts. (Default: "~/.datasystem/rocksdb")
# MASTER_BACKEND_STORE_DIR="~/.datasystem/rocksdb"

# The redis IP address host:port. If the redis service is required, the address must be set and match the worker's redis address. ex: 127.0.0.1:6379 (Default: "")
# MASTER_REDIS_ADDRESS=""

# maximum time interval before a node is considered lost (Default: "60")
# MASTER_NODE_TIMEOUT_S="60"

# maximum time interval for the master to determine node death (Default: "7200")
# MASTER_NODE_DEAD_TIMEOUT_S="7200"

# Interval in milliseconds at which master check heartbeat status (Default: "30000")
# MASTER_CHECK_HEARTBEAT_INTERVAL_MS="30000"

# Config rpc server thread number, must be greater than 0. (Default: "16")
# MASTER_RPC_THREAD_NUM="16"

# The directory to store unix domain socket file. The UDS generates temporary files in this path. (Default: "~/.datasystem/unix_domain_socket_dir")
# MASTER_UNIX_DOMAIN_SOCKET_DIR="~/.datasystem/unix_domain_socket_dir"

# The directory where log files are stored. (Default: "~/.datasystem/logs")
# MASTER_LOG_DIR="~/.datasystem/logs"

# Maximum log file size (in MB), must be greater than 0. (Default: "512")
# MASTER_MAX_LOG_SIZE="512"

# All log files max size (in MB), must be greater than 'MASTER_MAX_LOG_SIZE'. Log will roll if the size is exceeded. (Default: "10000")
# MASTER_TOTAL_LOG_SIZE_MB="10000"

# Flush log files with async mode. (Default: "false")
# MASTER_LOG_ASYNC="false"

# Compress old log files in .gz format. This parameter takes effect only when the size of the generated log is greater than max log size. (Default: "true")
# MASTER_LOG_COMPRESS="true"

# vlog level. (Default: "0")
# MASTER_V="0"

# Enable zmq authentication (Default: "false")
# MASTER_ZMQ_ENABLE_AUTH="false"

# The directory to find ZMQ curve key files. This path must be specified when zmq authentication is enabled. (Default: "")
# MASTER_CURVE_KEY_DIR=""
