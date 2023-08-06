#!/bin/bash
# Copyright (c) 2021 Huawei Technologies Co., Ltd
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

set -e

chown 1002:1002 /home/sn/log
chown 1003:1003 /home/snuser/log

sudo chown 1002:1002 /data
chmod 755 /data

sudo chown 1002:1002 /opt/function/code
chmod 755 /opt/function/code