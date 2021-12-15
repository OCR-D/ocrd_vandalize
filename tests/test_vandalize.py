from pathlib import Path

from ocrd import Resolver, Workspace
from ocrd_models.ocrd_page import parse
from ocrd_utils import pushd_popd

from ocrd_vandalize.processor import OcrdVandalize

def test_vandalize_textequiv():
    """Test whether text is changed"""
    resolver = Resolver()
    workspace_dir = str(Path(__file__).parent / 'assets/kant_aufklaerung_1784/data')
    with pushd_popd(workspace_dir):
        pcgts_before = parse('OCR-D-GT-PAGE/PAGE_0017_PAGE.xml')
        assert pcgts_before.get_Page().get_TextRegion()[0].get_TextLine()[0].get_TextEquiv()[0].Unicode == 'Berliniſche Monatsſchrift.'
        OcrdVandalize(
            Workspace(resolver, directory=workspace_dir),
            input_file_grp='OCR-D-GT-PAGE',
            output_file_grp='VANDALIZED').process()
        pcgts_after = parse('VANDALIZED/VANDALIZED_0001.xml')
        assert pcgts_after.get_Page().get_TextRegion()[0].get_TextLine()[0].get_TextEquiv()[0].Unicode != 'Berliniſche Monatsſchrift.'
