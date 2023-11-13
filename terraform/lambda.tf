resource "aws_lambda_function" "my_spotify_stats" {
  filename         = "../lambda.zip"
  function_name    = "my_spotify_stats"
  handler          = "lambda_function.lambda_handler"
  role             = aws_iam_role.lambda_execution_role.arn
  source_code_hash = filebase64sha256("../lambda.zip")
  runtime          = "python3.11"
  timeout          = 300

  environment {
    variables = {
      CLIENT_ID     = var.SPOTIFY_CLIENT_ID
      CLIENT_SECRET = var.SPOTIFY_CLIENT_SECRET
      REFRESH_TOKEN = var.SPOTIFY_REFRESH_TOKEN
    }
  }
}
