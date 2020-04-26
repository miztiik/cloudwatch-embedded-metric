# -*- coding: utf-8 -*-
"""
.. module: embedded_metric_log_generator.py
    :Actions: PUT cloudwatch embedded metric in cloudwatch logs
    :copyright: (c) 2020 Mystique.,
.. moduleauthor:: Mystique
.. contactauthor:: miztiik@github issues
"""

import time
import random
import copy
import json
import logging
import os

__author__ = 'Mystique'
__email__ = 'miztiik@github'
__version__ = '0.0.1'
__status__ = 'production'


class global_args:
    """ Global statics """
    OWNER = "Mystique"
    ENVIRONMENT = "production"
    MODULE_NAME = "embedded_metric_log_generator"
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()


def call_third_party_api():
    return _random_error_generator(n=os.getenv("PERCENTAGE_ERRORS", 75))


def _random_error_generator(n=75):
    """ Generate error for given n % """
    r = False
    if random.randint(1, 100) < int(n):
        time.sleep(1)
        r = True
    return r


def _set_metric(env, namespace, metric_name, metric_value, metric_unit="None", dimensions={}):
    """
    Generate custom metrics
    This works by printing into a specific JSON format documented here:
    https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Embedded_Metric_Format_Specification.html
    """

    retval = copy.deepcopy(dimensions)
    # Always inject 'Environment' as a dimension
    retval["Environment"] = env

    # Inject the embedded metric for CloudWatch
    # See https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Embedded_Metric_Format.html
    retval["_aws"] = {
        "CloudWatchMetrics": [{
            "Namespace": namespace,
            "Dimensions": [list(retval.keys())],
            "Metrics": [{
                "Name": metric_name,
                "Unit": metric_unit
            }]
        }],
        "Timestamp": int(time.time()*1000)
    }
    # Inject the metric value in the JSON blob
    retval[metric_name] = metric_value
    LOGGER.info(json.dumps(retval))
    return retval


def lambda_handler(event, context):
    global LOGGER
    LOGGER = logging.getLogger()
    LOGGER.setLevel(level=os.getenv("LOG_LEVEL", "INFO").upper())

    LOGGER.info(f"received_event:{event}")
    n_emf = {"ERROR": "Obviously something went wrong"}

    # Set a random default like, later over-ride if user provided info
    user_likes = random.randint(1, 100)
    # Grab likes from API Url path or set default values
    if event.get("pathParameters"):
        user_likes = event.get('pathParameters').get(
            'likes', random.randint(1, 100))

    if user_likes:
        n_emf = _set_metric(
            env=os.getenv("Environment", global_args.ENVIRONMENT),
            namespace="konstone-verse",
            metric_name="likes_counter",
            metric_value=int(user_likes),
            metric_unit="Count",
            dimensions={"_per_user_": "kon"}
        )

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": n_emf
        })
    }
