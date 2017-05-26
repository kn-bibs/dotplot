from collections import namedtuple
from tempfile import NamedTemporaryFile
import requests_mock
from pytest import raises
from dotplot.sequence import Sequence
from dotplot.sequence import DownloadFailed


def create_named_temp_file(data=''):
    temporary_file = NamedTemporaryFile(mode='w', delete=False)

    temporary_file.close()
    name = temporary_file.name

    with open(name, 'w') as f:
        f.write(data)

    return name


def test_load():

    valid_fasta = '>some_name\nACTGTACG'
    invalid_fasta = 'ACTGTACG'

    with open(create_named_temp_file(valid_fasta)) as valid_sequence_file:
        sequence = Sequence.from_fasta_file(valid_sequence_file)

        assert sequence.name == 'some_name'
        assert sequence.sequence == 'ACTGTACG'
        assert len(sequence) == 8

    with open(create_named_temp_file(invalid_fasta)) as invalid_sequence_file:
        with raises(TypeError):
            Sequence.from_fasta_file(invalid_sequence_file)


def test_download():

    test_datum = namedtuple('TestData', 'sequence_id url response sequence_name sequence constructor')

    test_data = [
        test_datum(
            'P03086',
            'http://www.uniprot.org/uniprot/P03086.fasta',
            (
                '>sp|P03086|AGNO_POVJC Agnoprotein OS=JC polyomavirus PE=1 SV=1\n'
                'MVLRQLSRKASVKVSKTWSGTKKRAQRILIFLLEFLLDFCTGEDSVDGKKRQRHSGLTEQ\n'
                'TYSALPEPKAT'
            ),
            'sp|P03086|AGNO_POVJC Agnoprotein OS=JC polyomavirus PE=1 SV=1',
            'MVLRQLSRKASVKVSKTWSGTKKRAQRILIFLLEFLLDFCTGEDSVDGKKRQRHSGLTEQTYSALPEPKAT',
            Sequence.from_uniprot
        )
    ]

    with requests_mock.mock(real_http=False) as mocked_requests:
        for data in test_data:
            mocked_requests.register_uri('GET', data.url, text=data.response)
            sequence = Sequence.from_uniprot(data.sequence_id)
            assert sequence.name == data.sequence_name
            assert sequence.sequence == data.sequence

        # as real_http is set to false, all requests other than registered will return 404
        mocked_requests.register_uri(
            'GET',
            'http://www.uniprot.org/uniprot/P00000.fasta',
            status_code=404
        )
        with raises(DownloadFailed):
            Sequence.from_uniprot('P00000')
