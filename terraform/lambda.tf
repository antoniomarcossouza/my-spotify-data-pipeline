resource "aws_lambda_layer_version" "requests" {
  filename            = "../requests.zip"
  layer_name          = "requests"
  source_code_hash    = filebase64sha256("../requests.zip")
  compatible_runtimes = ["python3.11"]
}
resource "aws_lambda_function" "my_spotify_stats" {
  filename         = "../lambda.zip"
  function_name    = "my_spotify_stats"
  handler          = "lambda_function.lambda_handler"
  role             = aws_iam_role.lambda_execution_role.arn
  source_code_hash = filebase64sha256("../lambda.zip")
  runtime          = "python3.11"
  timeout          = 300
  layers = ["arn:aws:lambda:us-east-2:336392948345:layer:AWSSDKPandas-Python311:3",
  "${aws_lambda_layer_version.requests.arn}"]

  environment {
    variables = {
      CLIENT_ID     = var.SPOTIFY_CLIENT_ID
      CLIENT_SECRET = var.SPOTIFY_CLIENT_SECRET
      REFRESH_TOKEN = var.SPOTIFY_REFRESH_TOKEN
    }
  }
}
