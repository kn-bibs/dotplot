from collections import namedtuple

import requests_mock
from pytest import raises

from dotplot.sequence import DownloadFailed
from dotplot.sequence import Sequence
from tests.miscellaneous import create_named_temp_file


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
        ),
        test_datum(
            'NP_001009852',
            'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=protein&rettype=fasta&id=NP_001009852',
            (
                '>NP_001009852.1 bladder cancer-associated protein [Felis catus]\n'
                'MYCLQWLLPVLLIPKPLNPALWFSHSMFMGFYLLSFLLERKPCTICALVFLAALFLICYSCWGNCFLYHC\n'
                'SDSPLPESAHDPGVVGT'
            ),
            'NP_001009852.1 bladder cancer-associated protein [Felis catus]',
            'MYCLQWLLPVLLIPKPLNPALWFSHSMFMGFYLLSFLLERKPCTICALVFLAALFLICYSCWGNCFLYHCSDSPLPESAHDPGVVGT',
            Sequence.from_ncbi
        ),
        test_datum(
            'ENSP00000200691',
            'https://rest.ensembl.org/sequence/id/ENSP00000200691',
            (
                '>ENSP00000200691\n'
                'MDPETCPCPSGGSCTCADSCKCEGCKCTSCKKSCCSCCPAECEKCAKDCVCKGGEAAEAE\n'
                'AEKCSCCQ'
            ),
            'ENSP00000200691',
            'MDPETCPCPSGGSCTCADSCKCEGCKCTSCKKSCCSCCPAECEKCAKDCVCKGGEAAEAEAEKCSCCQ',
            Sequence.from_ensembl
        )
    ]

    with requests_mock.mock(real_http=False) as mocked_requests:
        for data in test_data:
            mocked_requests.register_uri('GET', data.url, text=data.response)
            sequence = data.constructor(data.sequence_id)
            assert sequence.name == data.sequence_name
            assert sequence.sequence == data.sequence

        # as real_http is set to false, all requests other than registered will return 404
        mocked_requests.register_uri(
            'GET',
            'http://www.uniprot.org/uniprot/P00000.fasta',
            status_code=404
        )
        with raises(DownloadFailed) as exception:
            Sequence.from_uniprot('P00000')
        assert exception.value.message == 'After 3 attempts, download of P00000 sequence failed.'
