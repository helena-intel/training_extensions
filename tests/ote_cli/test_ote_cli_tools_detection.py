# Copyright (C) 2021 Intel Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions
# and limitations under the License.

import os
from subprocess import run

import pytest

from ote_cli.registry import Registry

from tests.ote_cli.common import collect_env_vars, get_some_vars, create_venv


args = {
    '--train-ann-file': 'data/airport/annotation_example_train.json',
    '--train-data-roots': 'data/airport/train',
    '--val-ann-file': 'data/airport/annotation_example_train.json',
    '--val-data-roots': 'data/airport/train',
    '--test-ann-files': 'data/airport/annotation_example_train.json',
    '--test-data-roots': 'data/airport/train',
}

root = '/tmp/ote_cli/'
ote_dir = os.getcwd()

templates = Registry('external').filter(task_type='DETECTION').templates
templates_names = [template['name'] for template in templates]


@pytest.mark.parametrize("template", templates, ids=templates_names)
def test_ote_train(template):
    work_dir, template_work_dir, algo_backend_dir = get_some_vars(template, root)
    create_venv(algo_backend_dir, work_dir, template_work_dir)
    command_line = ['ote',
                    'train',
                    template['path'],
                    '--train-ann-file',
                    f'{os.path.join(ote_dir, args["--train-ann-file"])}',
                    '--train-data-roots',
                    f'{os.path.join(ote_dir, args["--train-data-roots"])}',
                    '--val-ann-file',
                    f'{os.path.join(ote_dir, args["--val-ann-file"])}',
                    '--val-data-roots',
                    f'{os.path.join(ote_dir, args["--val-data-roots"])}',
                    '--save-weights',
                    f'{template_work_dir}/trained_{template["name"]}.pth',
                    'params',
                    '--learning_parameters.num_iters',
                    '2',
                    '--learning_parameters.batch_size',
                    '2']
    assert run(command_line, env=collect_env_vars(work_dir)).returncode == 0


@pytest.mark.parametrize("template", templates, ids=templates_names)
def test_ote_export(template):
    work_dir, template_work_dir, _ = get_some_vars(template, root)
    command_line = ['ote',
                    'export',
                    template['path'],
                    '--labels',
                    'none',
                    '--load-weights',
                    f'{template_work_dir}/trained_{template["name"]}.pth',
                    f'--save-model-to',
                    f'{template_work_dir}/exported_{template["name"]}']
    assert run(command_line, env=collect_env_vars(work_dir)).returncode == 0


@pytest.mark.parametrize("template", templates, ids=templates_names)
def test_ote_eval(template):
    work_dir, template_work_dir, _ = get_some_vars(template, root)
    command_line = ['ote',
                    'eval',
                    template['path'],
                    '--test-ann-file',
                    f'{os.path.join(ote_dir, args["--test-ann-files"])}',
                    '--test-data-roots',
                    f'{os.path.join(ote_dir, args["--test-data-roots"])}',
                    '--load-weights',
                    f'{template_work_dir}/trained_{template["name"]}.pth']
    assert run(command_line, env=collect_env_vars(work_dir)).returncode == 0


def test_notebook():
    work_dir = os.path.join(root, 'DETECTION')
    assert run(['pytest', '--nbmake', 'ote_cli/notebooks/train.ipynb', '-v'], env=collect_env_vars(work_dir)).returncode == 0
