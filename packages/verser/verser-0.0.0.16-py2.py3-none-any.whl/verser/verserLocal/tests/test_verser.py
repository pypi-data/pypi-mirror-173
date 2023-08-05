from verser.verserLocal.verser_ import *

import random


def test_create_version_instance():
    assert 4 + 4 == 8
    assert create_version_instance("1.0.17.2rc2") == VersionParts(1, 0, 17, 2, 2, True)
    assert create_version_instance("1.0.17.2") == VersionParts(1, 0, 17, 2, 0, False)
    assert create_version_instance("1.0.17.3rc4") == VersionParts(1, 0, 17, 3, 4, True)


def test_get_next_version(capsys):
    for item in range(3):
        inc = random.choice((True, False,))
        # inc = True
        pre = random.choice((True, False,))
        n = get_next_version(project=Project(version_file_path=Path("verser"),
                                             now_testing=True),
                             increment_=inc,
                             pre_release=pre,
                             verbose=True)
        assert n is not None
        with capsys.disabled():
            n = get_next_version(
                project=Project(now_testing=True),
                increment_=inc,
                pre_release=pre,
                verbose=True
            )
            assert n is not None


def test_get_current_version(capsys):
    for item in range(3):
        # inc = random.choice((True, False,))
        inc = True
        pre = random.choice((True, False,))
        # n = get_current_version(project=Project(), increment_=inc, pre_release=pre, verbose=True)
        # assert n is not None
        with capsys.disabled():
            n = get_current_version(project=Project(now_testing=True),
                                    verbose=True,
                                    now_testing=True
                                    )

            assert n is not None
