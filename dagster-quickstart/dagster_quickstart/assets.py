import json
import requests

import pandas as pd

from dagster import (
    MaterializeResult,
    MetadataValue,
    asset,
    define_asset_job,
    Definitions,
    job,
    op
)
from dagster_quickstart.configurations import HNStoriesConfig


@asset
def hackernews_top_story_ids(config: HNStoriesConfig):
    """Get top stories from the HackerNews top stories endpoint."""
    top_story_ids = requests.get("https://hacker-news.firebaseio.com/v0/topstories.json").json()

    with open(config.hn_top_story_ids_path, "w") as f:
        json.dump(top_story_ids[: config.top_stories_limit], f)


@asset(deps=[hackernews_top_story_ids])
def hackernews_top_stories(config: HNStoriesConfig) -> MaterializeResult:
    """Get items based on story ids from the HackerNews items endpoint."""
    with open(config.hn_top_story_ids_path, "r") as f:
        hackernews_top_story_ids = json.load(f)

    results = []
    for item_id in hackernews_top_story_ids:
        item = requests.get(f"https://hacker-news.firebaseio.com/v0/item/{item_id}.json").json()
        results.append(item)

    df = pd.DataFrame(results)
    df.to_csv(config.hn_top_stories_path)

    return MaterializeResult(
        metadata={
            "num_records": len(df),
            "preview": MetadataValue.md(str(df[["title", "by", "url"]].to_markdown())),
        }
    )




import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from torchvision import datasets
from torchvision.transforms import ToTensor

from ray import train
from ray.train.torch import TorchTrainer
from ray.train import ScalingConfig


def get_dataset():
    return datasets.FashionMNIST(
        root="/tmp/data",
        train=True,
        download=True,
        transform=ToTensor(),
    )


class NeuralNetwork(nn.Module):
    def __init__(self):
        super().__init__()
        self.flatten = nn.Flatten()
        self.linear_relu_stack = nn.Sequential(
            nn.Linear(28 * 28, 512),
            nn.ReLU(),
            nn.Linear(512, 512),
            nn.ReLU(),
            nn.Linear(512, 10),
        )

    def forward(self, inputs):
        inputs = self.flatten(inputs)
        logits = self.linear_relu_stack(inputs)
        return logits


# without distributed training, pure pytorch
def train_func():
    num_epochs = 3
    batch_size = 64

    dataset = get_dataset()
    dataloader = DataLoader(dataset, batch_size=batch_size)

    model = NeuralNetwork()

    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.SGD(model.parameters(), lr=0.01)

    for epoch in range(num_epochs):
        for inputs, labels in dataloader:
            optimizer.zero_grad()
            pred = model(inputs)
            loss = criterion(pred, labels)
            loss.backward()
            optimizer.step()
        print(f"epoch: {epoch}, loss: {loss.item()}")


# train_func()


# distributed training
def train_func_distributed():
    num_epochs = 3
    batch_size = 64

    dataset = get_dataset()
    dataloader = DataLoader(dataset, batch_size=batch_size)
    dataloader = train.torch.prepare_data_loader(dataloader)

    model = NeuralNetwork()
    model = train.torch.prepare_model(model)

    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.SGD(model.parameters(), lr=0.01)

    for epoch in range(num_epochs):
        for inputs, labels in dataloader:
            optimizer.zero_grad()
            pred = model(inputs)
            loss = criterion(pred, labels)
            loss.backward()
            optimizer.step()
        print(f"epoch: {epoch}, loss: {loss.item()}")


# For GPU Training, set `use_gpu` to True.
use_gpu = False


# @asset
# def trainer(num_workers=2):
#     trainer = TorchTrainer(
#         train_func_distributed,
#         scaling_config=ScalingConfig(num_workers=num_workers, use_gpu=use_gpu)
#     )

#     results = trainer.fit()
#     return results

from dagster import asset, Field, IntSource

@asset(config_schema={'num_workers': Field(IntSource, default_value=2, is_required=False)})
def trainer(context):
    num_workers = context.op_config['num_workers']
    use_gpu = False  # Assuming this is defined somewhere else or passed in similarly

    trainer = TorchTrainer(
        train_func_distributed,
        scaling_config=ScalingConfig(num_workers=num_workers, use_gpu=use_gpu)
    )

    results = trainer.fit()
    return results

# @op
# def trainer1(num_workers=2):
#     trainer = TorchTrainer(
#         train_func_distributed,
#         scaling_config=ScalingConfig(num_workers=num_workers, use_gpu=use_gpu)
#     )

#     results = trainer.fit()
#     return results



trainer_job = define_asset_job(name="trainer_job", selection="trainer")

