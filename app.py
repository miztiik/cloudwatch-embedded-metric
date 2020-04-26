#!/usr/bin/env python3

from aws_cdk import core

from cloudwatch_embedded_metric.cloudwatch_embedded_metric_stack import LambdaEmbeddedMetricsStack


app = core.App()
# Miztiik demonstration to show how to embed custom metrics alongside detailed log event data
miztiik_cloudwatch_embedded_metric_demo = LambdaEmbeddedMetricsStack(
    app,
    "cloudwatch-embedded-metrics",
    description="Miztiik demonstration to show how to embed custom metrics alongside detailed log event data"
)


# Stack Level Tagging
core.Tag.add(app, key="Owner",
             value=app.node.try_get_context('owner'))
core.Tag.add(app, key="OwnerProfile",
             value=app.node.try_get_context('github_profile'))
core.Tag.add(app, key="GithubRepo",
             value=app.node.try_get_context('github_repo_url'))
core.Tag.add(app, key="ToKnowMore",
             value=app.node.try_get_context('youtube_profile'))


app.synth()
