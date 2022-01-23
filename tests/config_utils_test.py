from config_utils import NameParser


def test_init():
    input_tup = ('filename1', 'filename2')
    example = NameParser(input_tup)
    assert example.input_files == input_tup


def test_determine_delim():
    under_tup = ('file_name',)
    under = NameParser(under_tup)
    under._NameParser__determine_delim()
    assert under.delim == '_'
    dash_tup = ('file-name',)
    dash = NameParser(dash_tup)
    dash._NameParser__determine_delim()
    assert dash.delim == '-'
    bad_tup = ('noknown', 'delims')
    bad = NameParser(bad_tup)
    bad._NameParser__determine_delim()
    assert bad.delim is None


def test_fields():
    files = ('one_5_monkey_cat_slinky',)
    fields_list = ['one', '5', 'monkey', 'cat', 'slinky']
    tf = NameParser(files)
    returned = tf._NameParser__fields()
    assert returned == fields_list
