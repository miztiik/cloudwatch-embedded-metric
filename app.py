#!/usr/bin/env python3

from aws_cdk import core

from lambda_embedded_metrics.lambda_embedded_metrics_stack import LambdaEmbeddedMetricsStack


app = core.App()
LambdaEmbeddedMetricsStack(app, "lambda-embedded-metrics")

app.synth()
