import os

import vcr

from tokenex import TokenExRequest

TOKENEX_USER_ID = "1234567890"
TOKENEX_API_KEY = "abcd123456"
FAKE_DATA = "4111111111111111"
FAKE_TOKEN = "4222222222221111"


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


def test_init():

    test_scheme = "nTOKENfour"
    test_headers = {
        "Test-Header": "TESTING"
    }

    tr = TokenExRequest(
        TOKENEX_USER_ID,
        TOKENEX_API_KEY,
        tokenex_test_mode=True,
        token_scheme_name=test_scheme,
        requests_options={"headers": test_headers}
    )

    assert tr.tokenex_id == TOKENEX_USER_ID
    assert tr.api_key == TOKENEX_API_KEY
    assert tr.tokenex_test_mode is True
    assert tr.token_scheme_name == test_scheme
    assert tr.token_scheme == TokenExRequest.TOKEN_SCHEMES[test_scheme]
    assert tr.requests_options['headers'] == test_headers

    return tr


def test_tokenize():

    tr = test_init()

    with MY_VCR.use_cassette('tokenize.yml'):
        result = tr.tokenize(FAKE_DATA)
        assert result.json['Success']


def test_tokenize_encrypted():

    tr = test_init()

    with MY_VCR.use_cassette('tokenize_encrypted.yml'):
        result = tr.tokenize_encrypted(FAKE_DATA)
        assert result.json['Success']


def test_validate():

    tr = test_init()

    with MY_VCR.use_cassette('validate.yml'):
        result = tr.validate(FAKE_TOKEN)
        assert result.json['Success']


def test_detokenize():

    tr = test_init()

    with MY_VCR.use_cassette('detokenize.yml'):
        result = tr.detokenize(FAKE_TOKEN)
        assert result.json['Success']
        assert result.json['Value'] == FAKE_DATA


def test_delete():

    tr = test_init()

    with MY_VCR.use_cassette('delete.yml'):
        result = tr.delete(FAKE_TOKEN)
        assert result.json['Success']
