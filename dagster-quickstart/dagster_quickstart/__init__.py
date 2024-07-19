from dagster import Definitions, load_assets_from_modules

from . import assets
from .assets import trainer_job

all_assets = load_assets_from_modules([assets])


defs = Definitions(
    assets=all_assets,
    jobs = [trainer_job],
)
