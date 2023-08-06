# Domino Low Code Assistant (LCA)

Toolbar assistant for Domino's Jupyter IDEs.

Accelerate routine data science tasks and smoothly interface with the Domino API through the LCA point-and-click GUI.

## Installation

Please see [Enabling LCA for Domino customers](https://docs.google.com/presentation/d/1a1md0ntWhSvna8swarGNoalfihjGF1ZndliS3eM0HM4/edit?usp=sharing) and the [Installation page of the LCA documentation](https://dominodatalab.github.io/low-code-jupyter-docs/install/)

***

## Technical notes

> For Python developers & Domino platform engineers

### Endpoint use via the [python-domino](https://github.com/dominodatalab/python-domino) package

   * `Domino._app_id`: Non public API, used in deployer to generate the app url ⚠️ https://github.com/dominodatalab/python-domino/issues/127
   * `Domino._Domino__app_get_status(app_id)`: Private API, used for deploying ⚠️: https://github.com/dominodatalab/python-domino/issues/128
   * `Domino.app_publish()`: Public API ✅.
   * `Domino.app_unpublish()`: Public API ✅.

### Endpoints used without API

   * `/v4/datasource/projects/`: To get the list of data sources. https://github.com/dominodatalab/python-domino/issues/129
   * `/u/{project_owner}/{project_name}/run/synchronizeRunWorkingDirectory/{run_id}` to sync the filesystem for deployment. https://github.com/dominodatalab/python-domino/issues/130
   * `/v4/users/self`: To get the user id for analytics.


## Running end-to-end test locally

Start a notebook server

   ```bash
   $ jupyter notebook --notebook-dir=tests/e2e/notebooks --NotebookApp.token='' --port=11112 --no-browser
   ```

Run tests

   ```bash
   $ py.test tests/e2e
   ```

Pass `--headed` or add the env var `PWDEBUG=1` for debugging.


## Developers

### Install

```
$ pip install -e .
# build lab extension
# (cd lcalabextension && npm install && npm run build)
# set up jupyter lab to symlink to in project build dir
$ jupyter labextension develop --overwrite low_code_assistant
# same for classic notebook
$ jupyter nbextension install --py --symlink --sys-prefix --overwrite low_code_assistant
```

### Jupyter Lab development

Run
```
$ (js lcalabextension; npm run watch)
```

And refresh Jupyter Lab when the build finishes (will auto-build when editing the source typescript).

### Classic Jupyter notebook

extension.js can be edited and has no build step, simply refresh the page after editing.
