# S3 bucket that works as a Helm chart repository
resource "aws_s3_bucket" "helm_charts" {
  bucket        = "${var.project_name}-helm-charts-${data.aws_caller_identity.current.account_id}"
  force_destroy = true
}

# Allow a public bucket policy (only for the charts/ folder, see below)
resource "aws_s3_bucket_public_access_block" "helm_charts" {
  bucket                  = aws_s3_bucket.helm_charts.id
  block_public_acls       = true
  ignore_public_acls      = true
  block_public_policy     = false
  restrict_public_buckets = false
}

# Anyone can download files from charts/ (Argo CD needs this)
data "aws_iam_policy_document" "helm_charts_public_read" {
  statement {
    sid       = "PublicReadCharts"
    actions   = ["s3:GetObject"]
    resources = ["${aws_s3_bucket.helm_charts.arn}/charts/*"]

    principals {
      type        = "*"
      identifiers = ["*"]
    }
  }
}

resource "aws_s3_bucket_policy" "helm_charts" {
  bucket     = aws_s3_bucket.helm_charts.id
  policy     = data.aws_iam_policy_document.helm_charts_public_read.json
  depends_on = [aws_s3_bucket_public_access_block.helm_charts]
}

# GitHub Actions may upload charts
data "aws_iam_policy_document" "github_actions_charts" {
  statement {
    sid       = "ChartsUpload"
    actions   = ["s3:PutObject", "s3:GetObject"]
    resources = ["${aws_s3_bucket.helm_charts.arn}/charts/*"]
  }

  statement {
    sid       = "ChartsList"
    actions   = ["s3:ListBucket"]
    resources = [aws_s3_bucket.helm_charts.arn]
  }
}

resource "aws_iam_role_policy" "github_actions_charts" {
  name   = "charts-upload"
  role   = aws_iam_role.github_actions.id
  policy = data.aws_iam_policy_document.github_actions_charts.json
}
