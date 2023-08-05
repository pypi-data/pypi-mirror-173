"""Pingdom class for Alert Exporter."""

import logging
from datetime import timedelta
from time import sleep

import pypingdom
from humanize import naturaldelta


class Pingdom:
    """
    A wrapper for the Cloudwatch boto client
    """

    def __init__(self, profile: str, region: str, debug: bool) -> None:
        client = pypingdom.Client(
            username="ops@skale-5.com",
            password="WozyikveDrytceu",
            apikey="9ue79sia6p86ei8nzn0ltxaaepldjp9i",
            email=None,
        )
        client.get_check()

    def init_client(self, profile: str, region: str) -> None:
        self.session = boto3.session.Session(profile_name=profile)
        self.client = self.session.client("cloudwatch", region_name=region)

    def build_rule_expression(self, rule: dict) -> str:
        if rule.get("ComparisonOperator") in [
            "GreaterThanUpperThreshold",
            "LessThanLowerThreshold",
        ]:
            metrics = {m["Id"]: m for m in rule["Metrics"]}
            c2 = metrics.pop(rule["ThresholdMetricId"])
            c1 = metrics.pop(next(iter(metrics)))
            if metrics:
                print("DEBUG: Hmmmm weird I didn't expect anything left here.")
            metric_name = c1["MetricStat"]["Metric"]["MetricName"]
            threshold = c2["Expression"]
            period = c1["MetricStat"]["Period"]
        else:
            metric_name = rule.get("MetricName")
            threshold = rule.get("Threshold")
            period = rule.get("Period")
        expression = (
            f"{metric_name}"
            f' {COMPARISON_OPERATORS[rule.get("ComparisonOperator")]}'
            f" {threshold}"
            f' for {rule.get("EvaluationPeriods")} datapoints within'
            f" {naturaldelta(timedelta(seconds=period))}"
        )
        return expression

    def get_alarms(self, profile: str, debug: bool) -> None:
        self.rules = []
        for region in self.regions:
            logging.info(f"Getting alarms from region {region}")
            try:
                self.init_client(profile=profile, region=region)
                alarms = self.client.describe_alarms()
            except botocore.exceptions.ClientError as e:
                logging.warning(f"Error while describing alarms in region {region}:")
                if debug:
                    print(e)
                continue
            for alarm_type in ["CompositeAlarms", "MetricAlarms"]:
                self.rules += [
                    {
                        "region": region,
                        "type": alarm_type,
                        "name": r.get("AlarmName", ""),
                        "description": r.get("AlarmDescription", ""),
                        "rule": self.build_rule_expression(rule=r),
                    }
                    for r in alarms[alarm_type]
                ]
            sleep(0.5)
