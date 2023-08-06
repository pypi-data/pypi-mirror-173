from install_def import install_def


def test_install_def():
    # empty requirements
    assert install_def("install_def")
    # requirements.txt
    assert install_def("import_definition")

def test_not_found():
    assert not install_def("fake_def")
