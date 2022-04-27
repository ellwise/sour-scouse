bucket = sour-scouse-chalice
stackname = sour-scouse-stack
region = us-east-1

delete:
	cd src/.package; \
	aws --region $(region) cloudformation delete-stack --stack-name $(stackname); \
	aws --region $(region) cloudformation wait stack-delete-complete --stack-name $(stackname); \
	aws s3 rb --force s3://$(bucket)/ --region $(region); \
	aws cloudformation describe-stacks --stack-name $(stackname) --query 'Stacks[0].StackStatus';

deploy:
	cd src/.package; \
	aws s3 mb s3://$(bucket)/ --region $(region); \
	aws cloudformation package \
		--template-file sam.json \
		--s3-bucket $(bucket) \
		--output-template-file sam-packaged.yaml; \
	aws --region $(region) cloudformation deploy \
		--template-file sam-packaged.yaml \
		--stack-name $(stackname) \
		--capabilities CAPABILITY_IAM; \
	aws --region $(region) cloudformation wait stack-create-complete --stack-name $(stackname); \
	aws --region $(region) cloudformation describe-stacks \
		--stack-name $(stackname) \
		--query 'Stacks[0].Outputs[3].OutputValue';

format:
	python -m black --config pyproject.toml .

install:
	pip install pip-tools
	pip-compile requirements.in
	pip install -r requirements.txt
	rm requirements.txt
	pip install -r src/requirements.txt

lint:
	python -m flake8 --config setup.cfg
	python -m black  --config pyproject.toml --check .

package:
	cd src; chalice package .package

run:
	cd src; chalice local

update:
	cd src/.package; \
	aws cloudformation package \
		--template-file sam.json \
		--s3-bucket $(bucket) \
		--output-template-file sam-packaged.yaml; \
	aws --region $(region) cloudformation deploy \
		--template-file sam-packaged.yaml \
		--stack-name $(stackname) \
		--capabilities CAPABILITY_IAM; \
	aws --region $(region) cloudformation wait stack-create-complete --stack-name $(stackname); \
	aws --region $(region) cloudformation describe-stacks \
		--stack-name $(stackname) \
		--query 'Stacks[0].Outputs[3].OutputValue';

venv:
	python -m venv venv
