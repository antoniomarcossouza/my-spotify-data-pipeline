resource "aws_cloudwatch_event_rule" "every_two_hours" {
  name                = "every-two-hours"
  description         = "Sends a trigger every two hours"
  schedule_expression = "rate(2 hours)"
  is_enabled          = false
}

resource "aws_cloudwatch_event_target" "trigger_cmo_strategy" {
  rule      = aws_cloudwatch_event_rule.every_two_hours.name
  target_id = "my_spotify_stats"
  arn       = aws_lambda_function.my_spotify_stats.arn
}
