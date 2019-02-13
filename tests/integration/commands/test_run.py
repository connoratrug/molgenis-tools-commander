import pytest

from tests.integration.utils import run_commander, entity_type_exists, package_exists


@pytest.mark.integration
def test_run(session):
    run_commander('run test_script')

    try:
        assert entity_type_exists(session, 'scripttest_testAutoId')
        assert package_exists(session, 'otherpackage')
    finally:
        session.delete('sys_md_Package', 'scripttest')
        session.delete('sys_md_Package', 'otherpackage')


@pytest.mark.integration
def test_run_error(session):
    with pytest.raises(SystemExit):
        run_commander('run test_script_error')

    try:
        assert package_exists(session, 'scripttest')
        assert not package_exists(session, 'package_after_error')
    finally:
        session.delete('sys_md_Package', 'scripttest')


@pytest.mark.integration
def test_run_ignore_error(session):
    run_commander('run test_script_error --ignore-errors')

    try:
        assert package_exists(session, 'scripttest')
        assert package_exists(session, 'package_after_error')
    finally:
        session.delete('sys_md_Package', 'scripttest')
        session.delete('sys_md_Package', 'package_after_error')
