"""Module for functions used throughout the test suite."""
import datetime
import random
from unittest.mock import MagicMock
from repomate import tuples

import constants


random.seed(41235)

GENERATE_REPO_URL = lambda repo_name, org_name: "{}/{}/{}".format(
    constants.HOST_URL, org_name, repo_name
)

RANDOM_DATE = lambda: (
    constants.FIXED_DATETIME
    - datetime.timedelta(
        days=random.randint(0, 1000),
        hours=random.randint(0, 1000),
        minutes=random.randint(0, 1000),
        seconds=random.randint(0, 1000),
    )
)


def raise_(exception):
    """Function meant for raising exceptions in lambda.

    Args:
        exception: An exception to raise (initialized object, not class)
    Returns:
        A function that raises the provided exception when called with any
        arguments.
    Usage:
        something = lambda: raise_(ValueError('bad value'))
    """

    def raise_exception(*args, **kwargs):
        raise exception

    return raise_exception


def to_magic_mock_issue(issue):
    """Convert an issue to a MagicMock with all of the correct
    attribuets."""
    mock = MagicMock()
    mock.user = MagicMock()
    mock.title = issue.title
    mock.body = issue.body
    mock.created_at = issue.created_at
    mock.number = issue.number
    mock.user = constants.User(issue.author)
    return mock


def from_magic_mock_issue(mock_issue):
    """Convert a MagicMock issue into a tuples.Issue."""
    return tuples.Issue(
        title=mock_issue.title,
        body=mock_issue.body,
        number=mock_issue.number,
        created_at=mock_issue.created_at,
        author=mock_issue.user.login,
    )