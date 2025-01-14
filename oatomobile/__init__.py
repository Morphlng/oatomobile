# Copyright 2020 The OATomobile Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""Public API for `oatomobile`."""

import os
import sys

from absl import logging

###############
# CARLA SETUP #
###############

# HACK(filangel): resolves https://github.com/carla-simulator/carla/issues/2132.
try:
  import torch
except ImportError:
  pass
try:
  import sonnet as snt
except ImportError:
  pass

# Enable CARLA PythonAPI to be accessed from `oatomobile`.
carla_path = os.getenv("CARLA_ROOT")
if carla_path is None:
  raise EnvironmentError(
      "Missing environment variable CARLA_ROOT, specify it before importing oatomobile"
  )

logging.debug("CARLA_ROOT={}".format(carla_path))
carla_python_api = os.path.join(
    carla_path,
    "PythonAPI",
    "carla",
)
if not os.path.exists(carla_python_api):
  raise ImportError("Missing CARLA installation at {}".format(carla_python_api))
sys.path.append(carla_python_api)

from agents.navigation.controller import VehiclePIDController  # pylint: disable=import-error
from agents.navigation.local_planner import \
    LocalPlanner  # pylint: disable=import-error
from agents.tools.misc import \
    compute_magnitude_angle  # pylint: disable=import-error
from agents.tools.misc import draw_waypoints  # pylint: disable=import-error
from agents.tools.misc import get_speed  # pylint: disable=import-error

# TODO: Carla changed this function into "is_within_distance"
# from agents.tools.misc import is_within_distance_ahead  # pylint: disable=import-error

# FIXME: This is a temporary fix for the above function.
import numpy as np
import math
def is_within_distance_ahead(target_location, current_location, orientation, max_distance):
    """
    Check if a target object is within a certain distance in front of a reference object.

    :param target_location: location of the target object
    :param current_location: location of the reference object
    :param orientation: orientation of the reference object
    :param max_distance: maximum allowed distance
    :return: True if target object is within max_distance ahead of the reference object
    """
    target_vector = np.array([target_location.x - current_location.x, target_location.y - current_location.y])
    norm_target = np.linalg.norm(target_vector)

    # If the vector is too short, we can simply stop here
    if norm_target < 0.001:
        return True

    if norm_target > max_distance:
        return False

    forward_vector = np.array(
        [math.cos(math.radians(orientation)), math.sin(math.radians(orientation))])
    d_angle = math.degrees(math.acos(np.dot(forward_vector, target_vector) / norm_target))

    return d_angle < 90.0

###############

# HACK(filangel): matplotlib setup - remove before release.
import matplotlib
matplotlib.use("Agg")

# Benchmarks API.
from oatomobile.benchmarks.carnovel.benchmark import carnovel
# Core API.
from oatomobile.core.agent import Agent
from oatomobile.core.benchmark import Benchmark
from oatomobile.core.dataset import Dataset
from oatomobile.core.dataset import Episode
from oatomobile.core.dataset import tokens
from oatomobile.core.loop import EnvironmentLoop
from oatomobile.core.registry import registry
from oatomobile.core.rl import Env
from oatomobile.core.rl import FiniteHorizonWrapper
from oatomobile.core.rl import Metric
from oatomobile.core.rl import MonitorWrapper
from oatomobile.core.rl import ReturnsMetric
from oatomobile.core.rl import SaveToDiskWrapper
from oatomobile.core.rl import StepsMetric
from oatomobile.core.simulator import Action
from oatomobile.core.simulator import Observations
from oatomobile.core.simulator import Sensor
from oatomobile.core.simulator import SensorSuite
from oatomobile.core.simulator import SensorTypes
from oatomobile.core.simulator import Simulator

# Public API.
__all__ = (
    # CARLA Python API
    "compute_magnitude_angle",
    "draw_waypoints",
    "is_within_distance_ahead",
    "LocalPlanner",
    "VehiclePIDController",
    # OATomobile core API
    "Agent",
    "Benchmark",
    "Dataset",
    "EnvironmentLoop",
    "Episode",
    "tokens",
    "registry",
    "Env",
    "FiniteHorizonWrapper",
    "Metric",
    "MonitorWrapper",
    "ReturnsMetric",
    "StepsMetric",
    "SaveToDiskWrapper",
    "Action",
    "Observations",
    "Sensor",
    "SensorSuite",
    "Simulator",
)

#  ASCII art borrowed from dm-haiku.
#  __________________________________________
# / Please don't use these symbols they      \
# \ are not part of the OATomobile public API. /
#  ------------------------------------------
#         \   ^__^
#          \  (oo)\_______
#             (__)\       )\/\
#                 ||----w |
#                 ||     ||
#
del os
del sys
del logging
del carla_path
del carla_python_api
try:
  del snt
except NameError:
  pass
try:
  del torch
except NameError:
  pass
