from tempfile import NamedTemporaryFile
from pytest import raises
from dotplot.sequence import Sequence


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

    with open(create_named_temp_file(invalid_fasta)) as invalid_sequence_file:
        with raises(TypeError):
            Sequence.from_fasta_file(invalid_sequence_file)
