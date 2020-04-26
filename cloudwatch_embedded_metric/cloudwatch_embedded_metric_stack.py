from aws_cdk import aws_logs as _logs
from aws_cdk import aws_lambda as _lambda
from aws_cdk import aws_apigateway as _apigw
from aws_cdk import core


class LambdaEmbeddedMetricsStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # The code that defines your stack goes here

        # Read Lambda Code):
        try:
            with open("cloudwatch_embedded_metric/lambda_src/embedded_metric_log_generator.py", mode="r") as f:
                konstone_embedded_metric_fn_code = f.read()
        except OSError:
            print("Unable to read Lambda Function Code")

        konstone_embedded_metric_fn = _lambda.Function(self,
                                                       "konstoneFunction",
                                                       function_name="konstone_embedded_metric_fn",
                                                       runtime=_lambda.Runtime.PYTHON_3_7,
                                                       handler="index.lambda_handler",
                                                       code=_lambda.InlineCode(
                                                           konstone_embedded_metric_fn_code),
                                                       timeout=core.Duration.seconds(
                                                           3),
                                                       reserved_concurrent_executions=1,
                                                       environment={
                                                           "LOG_LEVEL": "INFO"
                                                       }
                                                       )

        # Create Custom Loggroup
        # /aws/lambda/function-name
        konstone_lg = _logs.LogGroup(self,
                                     "konstoneLoggroup",
                                     log_group_name=f"/aws/lambda/{konstone_embedded_metric_fn.function_name}",
                                     removal_policy=core.RemovalPolicy.DESTROY
                                     )

        # Add API GW front end for the Lambda
        lambda_embedded_metrics_api_stage_options = _apigw.StageOptions(
            stage_name="myst",
            logging_level=_apigw.MethodLoggingLevel.INFO,
            # data_trace_enabled=True,
            metrics_enabled=True,
            # tracing_enabled=True # Enable if you want AWS Xray Tracing
        )

        # Create API Gateway
        api_01 = _apigw.LambdaRestApi(self, "lambda-embedded-metrics-api",
                                      rest_api_name="lambda-embedded-metrics-api",
                                      deploy_options=lambda_embedded_metrics_api_stage_options,
                                      handler=konstone_embedded_metric_fn,
                                      proxy=False)

        user_id = api_01.root.add_resource("user_id")
        add_user_likes = user_id.add_resource("{likes}")
        add_user_likes.add_method("GET")

        output_1 = core.CfnOutput(self,
                                  "lambda-embedded-metrics-url",
                                  value=f"{add_user_likes.url}",
                                  description="Use a browser to push the user likes to CW Logs, replace {likes} with your like value"
                                  )
