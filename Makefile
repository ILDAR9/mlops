SHELL=/bin/bash
# LOCAL_ENV=../base/env/bin/activate
LOCAL_ENV=env/bin/activate

# - extend with specific libs
# export PYTHONPATH=...
# export LD_LIBRARY_PATH=...

# - reduce CPU for onnx
# export OMP_NUM_THREADS=1

# - GPU parametrisation
export CUDA_VISIBLE_DEVICES=-1

ROOT=$(shell pwd)


##################
# Services monitor
##################

FLD_MONITOR_SERVICE=${ROOT}/services/monitoring

monitor_prepare:
	cd  ${FLD_MONITOR_SERVICE} && \
	python src/create_bucket.py

monitor_start:
	cd ${FLD_MONITOR_SERVICE} && \
	 docker compose up --build --force-recreate --always-recreate-deps --remove-orphans -d

monitor_stop:
	cd  ${FLD_MONITOR_SERVICE} && \
	 docker compose down

#######
# Other
#######

clean:
	rm -rf *.egg-info .eggs .pytest_cache dist .cache build
	rm -rf __pycache__

clear: clean

clean_dangling:
	docker rmi -f $(shell docker images -f "dangling=true" -q)

cls_cont:
	docker ps --no-trunc -a --filter "status=exited" -q | xargs docker container rm -f ./path/file