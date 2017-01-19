from dotplot.main import main


def test_main():
    # simple run test

    basic_cmd_sets = (
        ['./dotplot.py', '--fasta', '1.fa', '2.fa'],
        ['./dotplot.py', '--fasta', '1.fa', '2.fa', '--drawer', 'ascii'],
        ['./dotplot.py', '--fasta', '1.fa', '2.fa', '--window_size', '2'],
        ['./dotplot.py', '--fasta', '1.fa', '2.fa', '--window_size', '2', '--stringency', '2'],
        ['./dotplot.py', '--ncbi', 'NP_001009852', '--uniprot', 'P03086'],
    )

    for argv in basic_cmd_sets:
        assert main(argv)
