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
# AGENT_WORKER_ADDRESS="127.0.0.1:9088"

# Address of agent and the value cannot be empty. (Default: "127.0.0.1:9087")
# AGENT_ADDRESS="127.0.0.1:9087"

# Config rpc server thread number, must be greater than 0. (Default: "16")
# AGENT_RPC_THREAD_NUM="16"

# The directory to store unix domain socket file. The UDS generates temporary files in this path. (Default: "~/.datasystem/unix_domain_socket_dir")
# AGENT_UNIX_DOMAIN_SOCKET_DIR="~/.datasystem/unix_domain_socket_dir"

# The directory where log files are stored. (Default: "~/.datasystem/logs")
# AGENT_LOG_DIR="~/.datasystem/logs"

# Maximum log file size (in MB), must be greater than 0. (Default: "512")
# AGENT_MAX_LOG_SIZE="512"

# All log files max size (in MB), must be greater than 'MASTER_MAX_LOG_SIZE'. Log will roll if the size is exceeded. (Default: "10000")
# AGENT_TOTAL_LOG_SIZE_MB="10000"

# Flush log files with async mode. (Default: "false")
# AGENT_LOG_ASYNC="false"

# Compress old log files in .gz format. This parameter takes effect only when the size of the generated log is greater than max log size. (Default: "true")
# AGENT_LOG_COMPRESS="true"

# vlog level. (Default: "0")
# AGENT_V="0"

# Enable zmq authentication (Default: "false")
# AGENT_ZMQ_ENABLE_AUTH="false"

# The directory to find ZMQ curve key files. This path must be specified when zmq authentication is enabled. (Default: "")
# AGENT_CURVE_KEY_DIR=""
