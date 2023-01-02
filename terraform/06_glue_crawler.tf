resource "aws_glue_crawler" "gsheet_csv" {
  database_name = aws_glue_catalog_database.example.name
  name          = "gsheet_csv"
  role          = aws_iam_role.example.arn

  s3_target {
    path = "s3://${aws_s3_bucket.example.bucket}"
  }
}