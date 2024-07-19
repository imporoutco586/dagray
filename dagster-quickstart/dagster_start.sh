#!/bin/bash


export DAGSTER_HOME=/home/kaiyuan/Desktop/dag_ray/dagster-quickstart/envtest
cd /home/kaiyuan/Desktop/dag_ray/dagster-quickstart/
ray start --include-dashboard=True --head
dagster dev
