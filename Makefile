venv_activate:
	.venv3\Scripts\activate
install: venv_activate
	pip install -r requirements.txt