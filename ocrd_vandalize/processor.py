"""
Demonstrate the OCR-D Python API
"""
from PIL import ImageDraw, ImageFont
from text_styler import TextStyler

from ocrd import Processor
from ocrd_utils import (
    getLogger,
    make_file_id,
    assert_file_grp_cardinality,
    MIMETYPE_PAGE
)
from ocrd_models.ocrd_page import (
    to_xml,
    TextStyleType,
    AlternativeImageType,
)
from ocrd_modelfactory import page_from_file

from .constants import OCRD_TOOL, FONT


class OcrdVandalize(Processor):

    def __init__(self, *args, **kwargs):
        kwargs['ocrd_tool'] = OCRD_TOOL['tools']['ocrd-vandalize']
        kwargs['version'] = OCRD_TOOL['version']
        super(OcrdVandalize, self).__init__(*args, **kwargs)
        self. styler = TextStyler()

    def beautify(self, textequiv):
        textequiv.Unicode = self.styler.convert(textequiv.Unicode)

    def watermark_image(self, im, text, font_color):
        draw = ImageDraw.Draw(im)
        font = ImageFont.truetype(FONT, 100)

        width, height = im.size
        textwidth, textheight = draw.textsize(text, font)
        margin = 10
        x = (width - textwidth - margin) / 2
        y = (height - textheight - margin) / 2

        draw.text((x, y), text, font=font, fill=font_color)
        return im


    def process(self):
        """
        Replace TextEquiv/Unicode with randomly selected glyph equivalents from
        mathematical symbols in Unicode and watermark the image with a centered
        Fraktur slogan of your choice.
        """
        log = getLogger('ocrd_vandalize')
        assert_file_grp_cardinality(self.input_file_grp, 1)
        assert_file_grp_cardinality(self.output_file_grp, 1)
        font_color = self.parameter['font_color']
        text = self.parameter['text']
        for n, input_file in enumerate(self.input_files):
            page_id = input_file.pageId or input_file.ID
            file_id = make_file_id(input_file, self.output_file_grp)

            log.info('Processing: %d / %s of %d', n, page_id, len(list(self.input_files)))
            pcgts = page_from_file(self.workspace.download_file(input_file))
            page = pcgts.get_Page()
            pil_image, page_xywh, _ = self.workspace.image_from_page(page, page_id)
            file_id = make_file_id(input_file, self.output_file_grp)

            # Watermark the image and add as an AlternativeImage
            self.watermark_image(pil_image, text, font_color)
            pil_image_watermarked = self.workspace.save_image_file(pil_image, file_id + '.WATERMARKED',
                    page_id=input_file.pageId,
                    file_grp=self.output_file_grp)
            page.add_AlternativeImage(AlternativeImageType(filename=pil_image_watermarked, comments='%s,watermarked' % page_xywh['features']))

            # "beautify" the texts
            for textregion in page.get_AllRegions(classes=['Text'], depth=0, order='reading-order'):
                for textline in textregion.get_TextLine():  # pylint: disable=no-member
                    self.beautify(textline.get_TextEquiv()[0])
                    for word in textline.get_Word():
                        self.beautify(word.get_TextEquiv()[0])

            self.add_metadata(pcgts)
            pcgts.set_pcGtsId(file_id)
            self.workspace.add_file(
                ID=file_id,
                file_grp=self.output_file_grp,
                pageId=input_file.pageId,
                mimetype=MIMETYPE_PAGE,
                local_filename="%s/%s.xml" % (self.output_file_grp, file_id),
                content=to_xml(pcgts)
            )
