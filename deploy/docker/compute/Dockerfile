##
##  Copyright (c) 2019-2021, ETH Zurich. All rights reserved.
##
##  Please, refer to the LICENSE file in the root directory.
##  SPDX-License-Identifier: BSD-3-Clause
##
from f7t-base

ADD deploy/docker/compute/requirements.txt deps/requirements.txt
RUN pip3 install -r deps/requirements.txt

ADD src/compute/compute.py compute.py
ADD src/common/async_task.py async_task.py
ADD src/common/cscs_api_common.py cscs_api_common.py
ADD src/common/job_time.py job_time.py

ENTRYPOINT ["python3"]
CMD ["compute.py"]
