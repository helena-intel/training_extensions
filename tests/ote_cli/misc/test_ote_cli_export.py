"""Tests for input parameters with OTE CLI export tool"""
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


import pytest

from ote_sdk.test_suite.e2e_test_system import e2e_pytest_component

from ote_cli.utils.tests import (
    create_venv,
    get_some_vars,
)

from ote_cli_test_common import (
    wrong_paths,
    ote_common,
    logger,
    parser_templates,
    root,
)

params_values, params_ids, _, _ = parser_templates()


class TestExportCommon:
    @pytest.fixture()
    @e2e_pytest_component
    @pytest.mark.parametrize("back_end, template", params_values)
    def create_venv_fx(self, template):
        work_dir, template_work_dir, algo_backend_dir = get_some_vars(template, root)
        create_venv(algo_backend_dir, work_dir)

    @e2e_pytest_component
    @pytest.mark.parametrize("back_end, template", params_values, ids=params_ids)
    def test_ote_export_no_template(self, back_end, template, create_venv_fx):
        error_string = (
            "ote export: error: the following arguments are required:"
            " template, --load-weights, --save-model-to"
        )
        command_line = []
        ret = ote_common(template, root, "export", command_line)
        assert ret["exit_code"] != 0, "Exit code must not be equal 0"
        assert error_string in ret["stderr"], f"Different error message {ret['stderr']}"

    @e2e_pytest_component
    @pytest.mark.parametrize("back_end, template", params_values, ids=params_ids)
    def test_ote_export_no_weights(self, back_end, template, create_venv_fx):
        error_string = (
            "ote export: error: the following arguments are required: --load-weights"
        )
        command_line = [
            template.model_template_id,
            f"--save-model-to",
            f"./exported_{template.model_template_id}",
        ]
        ret = ote_common(template, root, "export", command_line)
        assert ret["exit_code"] != 0, "Exit code must not be equal 0"
        assert error_string in ret["stderr"], f"Different error message {ret['stderr']}"

    @e2e_pytest_component
    @pytest.mark.parametrize("back_end, template", params_values, ids=params_ids)
    def test_ote_export_no_save_to(self, back_end, template, create_venv_fx):
        error_string = (
            "ote export: error: the following arguments are required: --save-model-to"
        )
        command_line = [
            template.model_template_id,
            "--load-weights",
            f"./trained_{template.model_template_id}/weights.pth",
        ]
        ret = ote_common(template, root, "export", command_line)
        assert ret["exit_code"] != 0, "Exit code must not be equal 0"
        assert error_string in ret["stderr"], f"Different error message {ret['stderr']}"

    @e2e_pytest_component
    @pytest.mark.parametrize("back_end, template", params_values, ids=params_ids)
    def test_ote_export_wrong_path_load_weights(
        self, back_end, template, create_venv_fx
    ):
        error_string = "Path is not valid"
        for case in wrong_paths.values():
            command_line = [
                template.model_template_id,
                "--load-weights",
                case,
                f"--save-model-to",
                f"./exported_{template.model_template_id}",
            ]
            ret = ote_common(template, root, "export", command_line)
            assert ret["exit_code"] != 0, "Exit code must not be equal 0"
            assert (
                error_string in ret["stderr"]
            ), f"Different error message {ret['stderr']}"

    @e2e_pytest_component
    @pytest.mark.parametrize("back_end, template", params_values, ids=params_ids)
    def test_ote_export_wrong_path_save_model_to(
        self, back_end, template, create_venv_fx
    ):
        error_string = "Path is not valid"
        for case in wrong_paths.values():
            command_line = [
                template.model_template_id,
                "--load-weights",
                f"./trained_{template.model_template_id}/weights.pth",
                f"--save-model-to",
                case,
            ]
            ret = ote_common(template, root, "export", command_line)
            assert ret["exit_code"] != 0, "Exit code must not be equal 0"
            assert (
                error_string in ret["stderr"]
            ), f"Different error message {ret['stderr']}"
