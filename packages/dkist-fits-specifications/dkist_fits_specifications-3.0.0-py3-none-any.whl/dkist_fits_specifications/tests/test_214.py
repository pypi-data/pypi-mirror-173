from dkist_fits_specifications.spec214 import (
    expand_index_d,
    expand_index_k,
    load_expanded_spec214,
    load_full_spec214,
    load_spec214,
)
from dkist_fits_specifications.utils.frozendict import frozendict


def test_load_full_214():
    spec = load_full_spec214()
    visp = spec["visp"]
    assert "VSPNUMST" not in visp
    assert "VSPSTNUM" not in visp
    assert "IPTASK" not in spec["dkist-op"]
    assert isinstance(spec, frozendict)
    assert isinstance(spec["fits"], frozendict)
    assert isinstance(spec["fits"]["NAXIS"], frozendict)

    # No sections should be empty
    for key in spec:
        assert spec[key], f"The {key} section is empty"


def test_load_214():
    spec = load_spec214()
    assert isinstance(spec, frozendict)
    assert isinstance(spec["fits"], frozendict)
    assert isinstance(spec["fits"]["NAXIS"], frozendict)


def test_expand_k():
    spec = load_spec214()["dataset"]
    schema = expand_index_k(spec, DAAXES=2, DEAXES=1)
    assert "DINDEX3" in schema


def test_expand_d():
    spec = load_spec214()["dataset"]
    schema = expand_index_d(spec, NAXIS=2, DNAXIS=5)
    assert "DTYPE5" in schema


def test_expanded_schema():
    schemas = load_expanded_spec214(DAAXES=2, DEAXES=1, NAXIS=2, DNAXIS=5, INSTRUME="notthedkist")
    assert "DINDEX3" in schemas["dataset"]
    assert "NAXIS1" in schemas["fits"]
    assert "DTYPE5" in schemas["dataset"]


"""def test_spec_122_section():
    schemas = load_expanded_spec214(DAAXES=2, DEAXES=1, NAXIS=2, DNAXIS=5, INSTRUME="notthedkist")
    assert 'copy122' in schemas
    assert 'DATE-OBS' in schemas['copy122']"""
