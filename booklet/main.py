#!/usr/bin/env python3

# BSD 3-Clause License
#
# Copyright (c) 2022, HornPenguin Co.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from __future__ import annotations
import sys
import os

import pypdf

sys.path.insert(0, os.path.abspath("."))

from booklet.meta import __version__
from booklet.meta import name

from booklet.core.manuscript import Manuscript

from booklet.core.converters.toimage import ToImage

from booklet.core.templates.imposition import Imposition
from booklet.core.templates.printingmark import PrintingMark

from booklet.deprecated.converters import SigComposition, Signature

from booklet.utils.misc import get_page_range


# from booklet.data import *
from booklet.data import ( PaperFormat, beep_file, git_repository,
    homepage, icons, logo, tutorial
)

from booklet.utils.images import icon_path
from booklet.gui import Booklet
from booklet.parser import cli_parser as parser
from booklet.utils.conversion import pts2mm, mm2pts

# Misc utils
def check_dir(path_to_check):
    """
    Check passed path is a directory.
    """
    if os.path.isfile(path_to_check):
        return False
    if os.path.isdir(path_to_check):
        return True

    path_split = os.path.split(path_to_check)
    if os.path.isdir(path_split[0]):
        return False

    raise ValueError(f"Is {path_to_check} a path?")

def check_composition(sheets_per_section, pages_per_sheet):
    """
    Check the number of leaves/pages etc looks correct
    * Number of leaves per section must divide by 4.
    : nn - Number of pages printed on each original large sheet
    : ns - Number of such sheets inserted into each section
    """
    pages_per_section = pages_per_sheet * sheets_per_section
    if pages_per_section % 4 != 0:
        return False
    if pages_per_section == 4 and not sheets_per_section == 1:
        return False
    if pages_per_section == 12 and sheets_per_section not in [1, 3]:
        return False
    if pages_per_section == 24 and sheets_per_section not in [1, 2, 3, 6]:
        return False

    return True


def cal_blank_page(pages, leaves_per_section):
    """
    How many blank pages need to be added?
    * pages: Number of pages in document
    * leaves_per_section: Number of leaves per section
    """
    remainder = pages % leaves_per_section
    return (leaves_per_section - remainder) if leaves_per_section > 1 and remainder != 0 else 0


if __name__ == "__main__":
    args = parser.parse_args(sys.argv[1:])

    if args.console:  # console mode

        # Path validation
        input_file = ""
        outputpath = ""
        pagerange = ""
        if args.inputfile is not None:
            input_file = args.inputfile
        elif args.input is not None:
            input_file = args.input[0]
        elif args.format_help is None:
            raise ValueError("No input file")

        if args.outputpath is not None:
            outputpath = args.outputpath
        elif args.output is not None:
            outputpath = args.output[0]
        else:
            outputpath = os.getcwd()

        # name checker
        if check_dir(outputpath):
            if args.name is not None:
                name = args.name
            else:
                name_formatted = os.path.split(input_file)[1]
                name = name_formatted.split(".pdf")[0] + "_HP_BOOKLET" + ".pdf"
            outputpath = os.path.join(outputpath, name)

        pre_pdf = pypdf.PdfReader(input_file)
        page_max = len(pre_pdf.pages)
        default_size = [
            float(pre_pdf.pages[0].mediabox.width),
            float(pre_pdf.pages[0].mediabox.height),
        ]

        # page range
        if args.page_range is not None:
            for li in args.page_range:
                st = "".join(li)
                pagerange += st
        else:
            pagerange = f"1-{page_max}"

        # toimage
        toimagebool = args.toimage

        # riffle
        rifflebool = True
        if args.riffle_direction == "left":
            rifflebool = False

        # format setting
        if args.format is None or args.format == "Default":
            width, height = pts2mm(default_size)
            format_mm = [width, height]
            paper_format = default_size
        else:
            format_size = PaperFormat[args.format[0]].split("x")
            format_mm = [float(format_size[0]), float(format_size[1])]
            paper_format = [mm2pts(format_mm)]

        # sig composition
        nl = args.sig_composition[0]
        nn = args.sig_composition[1]
        ns = int(nl / nn)
        print(f"Leaves: nl:{nl}, nn:{nn}, ns:{ns}")
        if not check_composition(nn, ns):
            raise ValueError(f"sig composition {nl} {nn} are not vaild.")
        # nl = nn * ns
        _sig_composition = SigComposition(nl, nn)

        # blank
        blankmode = args.blank_mode
        blank = [blankmode, cal_blank_page(len(get_page_range(pagerange)), nl)]

        # sigproof
        if args.sigproof is not None:
            sigproof = [True, args.sigproof]
        else:
            sigproof = [False, [0,0,0,0]]

        printbool = args.crop or args.registration or args.cmyk or sigproof[0]

        # Print work info
        print(f"Input:               {input_file}")
        print(f"output:              {outputpath}")
        print(f"page range:          {pagerange}")
        print(f"Adding               {blank[1]} blank pages to the {blank[0]}")
        print("signature composition:")
        print(f"  Pages              {nl} per signature")
        print(f"  inserting          {nn} x {ns} page sub signatures")
        print(f"riffle direction:    {args.riffle_direction}")
        print(f"paper format:        {args.format} {format_mm[0]}x{format_mm[1]} (mm)")
        print(f"fold:                {args.fold}")
        print(f"imposition:          {args.imposition}")
        print(f"split per signature: {args.split}")
        print(f"sigproof:            {sigproof[0]} colour={args.sigproof}")
        print(f"crop/trim:           {args.crop}")
        print(f"reg                  {args.registration}")
        print(f"cmyk                 {args.cmyk}")

        if not args.y:
            print("Continue?(Y/N):")
            answer = input()
            if answer[0] not in ("y", "Y"):
                sys.exit()

        # old code
        # pages = sig.get_exact_page_range(pagerange=pagerange, blank=blank)
        # page_len =len(pages) * (2 if printbool or args.imposition else 1)

        # generate----------------------------

        default_gap = 5
        default_margin = 43

        print(f"input_file:{input_file}, outputpath:{outputpath}")
        manuscript = Manuscript(
            input_file=input_file,
            output_file=os.path.dirname(outputpath),
            filename=os.path.basename(outputpath),
            page_range=pagerange
        )

        toimage = ToImage(toimage=toimagebool, dpi=600)

        signature = Signature(
            sig_composition=_sig_composition,
            blank_mode=blankmode,
            riffle=rifflebool,
            fold=args.fold,
            paper_format=paper_format,
        )
        print(f"sigproof:{sigproof}")
        imposition = Imposition(
            imposition=args.imposition,
            gap=default_gap,
            proof=sigproof[0],
            proof_color=sigproof[1],
            proof_width=default_gap * 2,
            imposition_layout=_sig_composition,
        )
        printing_mark = PrintingMark(
            on=bool(args.crop or args.registration or args.cmyk),
            margin=default_margin,
            crop=args.crop,
            reg=args.registration,
            cmyk=args.cmyk,
        )
        modifiers = [toimage, signature, imposition, printing_mark]
        for modifier in modifiers:
            manuscript.modifier_register(modifier)
        manuscript.update(do="all", file_mode="unsafe")
        if args.split:
            print(f"_sig_composition: {_sig_composition.composition}")
            manuscript.save_to_file(split=_sig_composition.composition[0]*2)
        else:
            manuscript.save_to_file()

        # sig.generate_signature(
        #    inputfile=inputfile,
        #    output=outputpath,
        #    pagerange=pagerange,
        #    blank=blank,
        #    sig_com=sig_composition,
        #    riffle=rifflebool,
        #    fold=True if args.imposition else args.fold,
        #    format=format,
        #    imposition=args.imposition,
        #    split=args.split,
        #    trim=args.trim,
        #    registration=args.registration,
        #    cmyk=args.cmyk,
        #    sigproof=sigproof,
        #    progress=[page_len]
        # )

        print("\n")
        print(f"Done {os.path.split(outputpath)[1]}.")
    else:  # guid mode
        text_pady = 3

        hpbooklet = Booklet(
            icon_path,
            homepage=homepage,
            source=git_repository,
            tutorial=tutorial,
            textpady=text_pady,
            beep_file=beep_file,
            logo=logo,
            icons=icons,
        )
        hpbooklet.window.mainloop()
