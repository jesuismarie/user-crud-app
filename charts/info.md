```bash
	helm template charts/user-crud-app \
	--set image.repository="$(terraform -chdir=infra/terraform output -raw ecr_repository_url)" \
	--set image.tag=1.0.0
```

Push the first image by hand (once the repository exists):

```
   ECR=$(terraform -chdir=infra/terraform output -raw ecr_repository_url)
   aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin "${ECR%%/*}"
   docker build -t "$ECR:1.0.0" -f app/backend/Dockerfile app
   docker push "$ECR:1.0.0"
```