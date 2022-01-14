from pathlib import Path
from filecmp import cmp

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

def test_vandalize_image():
    """Test whether image is changed"""
    resolver = Resolver()
    workspace_dir = str(Path(__file__).parent / 'assets/kant_aufklaerung_1784/data')
    with pushd_popd(workspace_dir):
        workspace = Workspace(resolver, directory=workspace_dir)
        file_before = list(workspace.mets.find_files(fileGrp='OCR-D-GT-PAGE',
                                                     pageId='PHYS_0017'))
        img_before = list(workspace.mets.find_files(fileGrp='OCR-D-IMG',
                                                     pageId='PHYS_0017'))
        assert len(file_before) == 1
        assert len(img_before) == 1
        pcgts_before = parse(file_before[0].url)
        OcrdVandalize(workspace,
                      input_file_grp='OCR-D-GT-PAGE',
                      output_file_grp='VANDALIZED').process()
        file_after = list(workspace.mets.find_files(fileGrp='VANDALIZED',
                                                    pageId='PHYS_0017',
                                                    mimetype='application/vnd.prima.page+xml'))
        assert len(file_after) == 1
        pcgts_after = parse(file_after[0].url)
        assert pcgts_after.get_Page().get_TextRegion()[0].get_TextLine()[0].get_TextEquiv()[0].Unicode != 'Berliniſche Monatsſchrift.'
        img_after = list(workspace.mets.find_files(fileGrp='VANDALIZED',
                                                   pageId='PHYS_0017',
                                                   mimetype='image/png'))
        assert len(img_after) == 1
        altimg_after = pcgts_after.get_Page().get_AlternativeImage()
        assert len(altimg_after) == 1
        assert 'watermarked' in altimg_after[-1].get_comments()
        assert img_after[0].url == altimg_after[-1].get_filename()
        assert not cmp(img_before[0].url, img_after[0].url, shallow=False)
