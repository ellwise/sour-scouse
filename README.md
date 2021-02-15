# sour-scouse

To install dependencies
1. Create a virtual environment using `python -m venv venv`
2. Generate a package requirements file using `pip install pip-compile` then `pip-compile`
3. Install the requirements using `pip install -r requirements.txt`

After making code changes 
1. Run `black .` to format code before pushing changes to GitHub

To deploy
1. Ensure that `run.py` is using `debug=False` in the `run_server` command
2. Create an S3 bucket called `sour-scouse`
3. Ensure AWS credentials are in `~/.aws/credentials` (if needed, these can be added by running `aws configure`)
4. Run `zappa deploy production`
5. To update the deployed code without changing the underlying routes, run `zappa update production`
6. To associate with an SSL certificate run `zappa certify` - note that this uses the `certificate_arn` in `zappa_settings.yml` and that it must be in the `us-east-1` region

To undeploy
1. Run `zappa undeploy production`

Notes:
* `zappa` has a bug when `slim_handler` is used - see [here](https://github.com/Miserlou/Zappa/issues/776] - this is fixed by removing `'libmysqlclient.so.18'` from `./venv/lib/python3.7/site-packages/zappa/handler.py:105`
