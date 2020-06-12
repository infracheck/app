def test_regex_cmd(host):
    import re
    out = host.run('echo hello').stdout

    assert re.search('hello', out), "Output: '" + out + "'does not contain regex: '" + 'hello' + "'"
