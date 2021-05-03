import numpy as np
import pytest
import torch
import random
import string

from continuum.datasets import InMemoryDataset
from continuum.scenarios import ClassIncremental
from continuum.generators import TaskOrderGenerator


def gen_data():
    x_train = np.random.randint(0, 255, size=(20, 32, 32, 3))
    y_train = []
    for i in range(10):
        y_train.append(np.ones(2) * i)
    y_train = np.concatenate(y_train)

    x_test = np.random.randint(0, 255, size=(20, 32, 32, 3))
    y_test = np.copy(y_train)

    return (x_train, y_train), (x_test, y_test)


def test_task_order_generator():
    train, test = gen_data()
    dummy = InMemoryDataset(*train)
    scenario = ClassIncremental(dummy, increment=1)

    scenario_generator = TaskOrderGenerator(scenario)
    sample_scenario = scenario_generator.sample()

    assert sample_scenario.nb_tasks == scenario.nb_tasks


@pytest.mark.parametrize("seeds", [
    [0, 1],
    [1664, 41],
    [1792, 1992]
])
def test_task_order_generator_seed(seeds):
    train, test = gen_data()
    seed_0 = seeds[0]
    seed_1 = seeds[1]
    dummy = InMemoryDataset(*train)
    scenario = ClassIncremental(dummy, increment=1)

    scenario_generator = TaskOrderGenerator(scenario)
    task_order_0 = scenario_generator.get_class_order(seed=seed_0)
    task_order_1 = scenario_generator.get_class_order(seed=seed_1)
    task_order_0_2 = scenario_generator.get_class_order(seed=seed_0)

    assert not torch.all(task_order_0.eq(task_order_1))
    assert torch.all(task_order_0.eq(task_order_0_2))


@pytest.mark.parametrize("nb_tasks", [
    2,
    4
])
def test_task_order_generator_nb_tasks(nb_tasks):
    train, test = gen_data()
    dummy = InMemoryDataset(*train)
    scenario = ClassIncremental(dummy, increment=1)
    scenario_generator = TaskOrderGenerator(scenario)
    sample_scenario = scenario_generator.sample(nb_tasks=nb_tasks)

    assert sample_scenario.nb_tasks == nb_tasks