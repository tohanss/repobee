import os
import pytest
from gits_pet import config
from gits_pet import exception

STUDENTS = pytest.constants.STUDENTS
USER = pytest.constants.USER
GITHUB_BASE_URL = pytest.constants.GITHUB_BASE_URL
ORG_NAME = pytest.constants.ORG_NAME


class TestGetConfiguredDefaults:
    """Tests for get_configured_defaults"""

    def test_get_configured_defaults_no_config_file(self, isfile_mock):
        defaults = config.get_configured_defaults()
        assert not defaults

    def test_get_configured_defaults_empty_file(self, empty_config_mock):
        with pytest.raises(exception.FileError) as exc_info:
            defaults = config.get_configured_defaults()
        assert "does not contain the required [DEFAULTS] header" in str(
            exc_info)

    def test_get_configured_defaults_reads_full_config(self, config_mock,
                                                       students_file):
        defaults = config.get_configured_defaults()
        assert defaults['user'] == USER
        assert defaults['github_base_url'] == GITHUB_BASE_URL
        assert defaults['org_name'] == ORG_NAME
        assert defaults['students_file'] == str(students_file)

    def test_get_configured_defaults_raises_on_invalid_keys(
            self, empty_config_mock, students_file):
        invalid_key = "not_valid_key"
        config_contents = os.linesep.join([
            "[DEFAULTS]",
            "github_base_url = {}".format(GITHUB_BASE_URL),
            "user = {}".format(USER),
            "org_name = {}".format(ORG_NAME),
            "students_file = {!s}".format(students_file),
            "{} = whatever".format(invalid_key),
        ])
        empty_config_mock.write(config_contents)

        with pytest.raises(exception.FileError) as exc_info:
            config.get_configured_defaults()

        assert "invalid keys" in str(exc_info)
        assert invalid_key in str(exc_info)

    def test_get_configured_defaults_raises_on_missing_header(
            self, empty_config_mock, students_file):
        config_contents = os.linesep.join([
            "github_base_url = {}".format(GITHUB_BASE_URL),
            "user = {}".format(USER),
            "org_name = {}".format(ORG_NAME),
            "students_file = {!s}".format(students_file),
        ])
        empty_config_mock.write(config_contents)

        with pytest.raises(exception.FileError) as exc_info:
            config.get_configured_defaults()

        assert "does not contain the required [DEFAULTS] header" in str(
            exc_info)