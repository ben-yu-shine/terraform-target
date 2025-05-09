.PHONY: build-venv activate-venv terraform-target build clean

build-venv:
	@pipenv sync --dev

activate-venv:
	@pipenv shell --python 3.12

terraform-target:
	@pipenv run python terraform_target/main.py --tf-file=$(TF_FILE) --env=$(ENV) --env-id=$(ENV_ID) --action=$(ACTION)

build: clean
	@pipenv run python -m build

install: build
	pip install dist/terraform_target-0.10.0-py3-none-any.whl

uninstall:
	pip uninstall dist/terraform_target-0.10.0-py3-none-any.whl -y

clean:
	rm -rf ./dist
	rm -rf ./terraform_target.egg-info
