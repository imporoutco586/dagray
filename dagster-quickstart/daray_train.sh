#!/bin/bash
source activate py38
cd /home/kaiyuan/Desktop/dag_ray/dagster-quickstart
export DAGSTER_HOME=/home/kaiyuan/Desktop/dag_ray/dagster-quickstart/envtest

dagster job execute -m dagster_quickstart -j trainer_job -c dagster_quickstart/config.yaml
dagster job execute -m dagster_quickstart -j trainer_job 