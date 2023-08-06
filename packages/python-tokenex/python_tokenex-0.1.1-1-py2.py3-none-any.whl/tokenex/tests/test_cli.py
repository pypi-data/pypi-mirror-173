import os

import argparse
import vcr

import tokenex.cli


CASSETTE_DIR = os.path.join(
    os.path.dirname(
        os.path.realpath(__file__)
    ),
    'fixtures', 'cassettes'
)

MY_VCR = vcr.VCR(
    cassette_library_dir=CASSETTE_DIR,
    record_mode='none',
    filter_post_data_parameters=['APIKey', 'TokenExID']
)


def test_cli_tokenize():
    args = argparse.Namespace(
        action="tokenize",
        value="4111111111111111",
        user_id="1234567890",
        api_key="abcd123456",
        token_scheme="nTOKENfour",
        test_mode=True
    )

    with MY_VCR.use_cassette('tokenize.yml'):
        tokenex.cli.main(args)


def test_cli_tokenize_encrypted():
    args = argparse.Namespace(
        action="tokenize_encrypted",
        value="4111111111111111",
        user_id="1234567890",
        api_key="abcd123456",
        token_scheme="nTOKENfour",
        test_mode=True
    )

    with MY_VCR.use_cassette('tokenize_encrypted.yml'):
        tokenex.cli.main(args)


def test_cli_detokenize():
    args = argparse.Namespace(
        action="detokenize",
        value="4111111111111111",
        user_id="1234567890",
        api_key="abcd123456",
        token_scheme="nTOKENfour",
        test_mode=True
    )

    with MY_VCR.use_cassette('detokenize.yml'):
        tokenex.cli.main(args)


def test_cli_validate():
    args = argparse.Namespace(
        action="validate",
        value="4111111111111111",
        user_id="1234567890",
        api_key="abcd123456",
        token_scheme="nTOKENfour",
        test_mode=True
    )

    with MY_VCR.use_cassette('validate.yml'):
        tokenex.cli.main(args)


def test_cli_delete():
    args = argparse.Namespace(
        action="delete",
        value="4111111111111111",
        user_id="1234567890",
        api_key="abcd123456",
        token_scheme="nTOKENfour",
        test_mode=True
    )

    with MY_VCR.use_cassette('delete.yml'):
        tokenex.cli.main(args)


def test_validate_args():
    args = argparse.Namespace(
        action="delete",
        value="4111111111111111",
        user_id="1234567890",
        api_key="abcd123456",
        token_scheme="nTOKENfour",
        test_mode=True
    )

    errors = tokenex.cli.validate_args(args)
    assert len(errors) == 0


def test_validate_args_error():
    args = argparse.Namespace(
        action="delete",
        value="4111111111111111",
        user_id=None,
        api_key="abcd123456",
        token_scheme="nTOKENfour",
        test_mode=True
    )

    errors = tokenex.cli.validate_args(args)
    assert len(errors) == 1


def test_validate_args_testmode():
    args = argparse.Namespace(
        action="delete",
        value="4111111111111111",
        user_id="1234567890",
        api_key="abcd123456",
        token_scheme="nTOKENfour",
        test_mode=None
    )

    errors = tokenex.cli.validate_args(args)
    assert len(errors) == 0
    assert args == argparse.Namespace(
        action="delete",
        value="4111111111111111",
        user_id="1234567890",
        api_key="abcd123456",
        token_scheme="nTOKENfour",
        test_mode=False
    )


def test_validate_args_testmode_envar():
    args = argparse.Namespace(
        action="delete",
        value="4111111111111111",
        user_id="1234567890",
        api_key="abcd123456",
        token_scheme="nTOKENfour",
        test_mode=None
    )
    os.environ['TOKENEX_TEST_MODE'] = "True"
    errors = tokenex.cli.validate_args(args)
    assert len(errors) == 0
    assert args == argparse.Namespace(
        action="delete",
        value="4111111111111111",
        user_id="1234567890",
        api_key="abcd123456",
        token_scheme="nTOKENfour",
        test_mode=True
    )


def test_validate_args_testmode_envar_true():
    args = argparse.Namespace(
        action="delete",
        value="4111111111111111",
        user_id="1234567890",
        api_key="abcd123456",
        token_scheme="nTOKENfour",
        test_mode=None
    )
    os.environ['TOKENEX_TEST_MODE'] = "False"
    errors = tokenex.cli.validate_args(args)
    assert len(errors) == 0
    assert args == argparse.Namespace(
        action="delete",
        value="4111111111111111",
        user_id="1234567890",
        api_key="abcd123456",
        token_scheme="nTOKENfour",
        test_mode=False
    )
