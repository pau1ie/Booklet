============================
Terms of Book and Printing
============================

This document describes basic bookbinding and printing terms.
More detailed descriptions, algorithms and implementations are contained
in :ref:`Features <features>`.


Shape and Structure of Book
==================================

Bookbinding is the process of binding materials to make a book. To
discuss how to make a book we need to agree how terms are defined.


Page
----

A page is defined as one side of a leaf. So where pages are numbered,
each page has it's own number.


Leaf
----

A leaf contains two pages, one on each side.


Sheet
-----

A piece of paper. The fact a sheet of paper can be cut into smaller
sheets means that we need to be specific about what type of sheet
we are referring to. Inside a section a sheet is two leaves folded
and usually sewn together with the other sheets in the section. A larger
sheet may have been used being folded and cut as described below
to create these smaller sheets that are part of a section.


Signature
-----------

A group of sheets sewn together. 
The **signature** is a contents block of a book, pamphlet, or booklet. 
There are some synonyms, **section**, and **gathering**. This document
will use **signature**.

Pages compose a signature and the signatures compose a book, booklet,
..., et cetera.
A single page can become a signature and a single singnature can compose
a single book or booklet, (usually booklet).


Text Block
----------

One or more signatures are gathered together forming the text block,
which is the complete contents of the book.


Why are signatures required in bookbinding? 
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Single-signature books are limited in size, as each sheet needs to fit
around the other folded sheets. The more sheets that are added to a
section, the more the inside pages need to be trimmed to make the leaves
line up with each other.

If books are being constructed from larger sheets of paper which are then
folded and cut, it is often convenient to form a signature from this process.
The sizes are listed below.


Types of signature
^^^^^^^^^^^^^^^^^^^^^^

By the number of leaves
""""""""""""""""""""""""""""
Commonly used types are next,

+-------------------+-------+---------+-------+
|Name               |Pages  |Leaves   | Folds |
+===================+=======+=========+=======+
|folio              |4      |2        | 1     |
+-------------------+-------+---------+-------+
|quartos            |8      |4        | 2     |
+-------------------+-------+---------+-------+
|octavo             |16     |8        | 3     |
+-------------------+-------+---------+-------+
|duodecimo(12mo)    |48     |24       | \*    |
+-------------------+-------+---------+-------+
|16mo               |64     |32       | 5     |
+-------------------+-------+---------+-------+
|18mo               |72     |36       | \*    |
+-------------------+-------+---------+-------+
|32mo               |128    |64       | 6     |
+-------------------+-------+---------+-------+
|64mo               |256    |128      | 7     |
+-------------------+-------+---------+-------+

\* See Extended type below.

While the above mentioned names indicate leaves of each signature,
they can also indicate the size of the book, if the original paper
size is known. The country's standard the raw paper size is used,
unless stated otherwise.

For example, Crown quartos size, 195 x 254 (mm), is a quarter of Crown
paper size, 508 x 381 (mm).


Imposition
-------------

Imposition is the process of printing pages on to a large sheet such that
once it is folded the pages appear in the correct order.
Apart from book binding in the old Asian style (this method can use single 
paper as a basic signature), the manuscript for a book
has a number of pages which is a multiple of 4.

Varying the direction and order of the folds will require changing 
the imposition layout on the larger paper to ensure the pages end
up in the correct order.
If you have experience of map folding in origami geometry, this will
be familiar. 
However, signature folding is not as complex, because the signatures
must end up with a centre fold where they are all sewn together. 


**Signature folding**

* Every fold must be perpendicular or parallel to every other fold.
* Each fold must be:
   1. (\*) Perpendicular to the previous fold line and fold all layers.
   2. (\**), Parallel to the previous fold line and fold all layers.
   3. (\*\*\*), Parallel to the previous fold line. If not all layers
      are folded, the rest must be folded in the same stage. 
      Sequential parallel folds can include a proportion of the layers, 
      in which case, there must be other parallel folding steps.

      For example, a sheet can be folded into three in concertina
      (zig zag) style by making a mountain fold and a valley fold.
      Or it can be folded into three in envelope style by making
      two parallel valley folds.

* The last fold must be (\*) or (\*\*) type.

| (\*), (\**) : Doubling previous grids.
| (\*\*\*) : :math:`k` number of parallel partial folding makes :math:`{} \times (k+1)` grids.


Standard type
^^^^^^^^^^^^^^^^^
Repetation of 1st type folding only.
Leaves = :math:`2^n`, i.e. 2, 4, 8, 16, 32, 64, 128, ... .


Extended type
^^^^^^^^^^^^^^^^^

At least one step is 2nd type folding, this allows us to compose
addtional prime numbers for divisor of leaves number.

Example: 6, 12 

6 leaves:

* Fold :math:`x`-direction - start
* Parallel fold :math:`x`-direction - end :math:`{} \times 3`
* Perpendicular fold :math:`y`-direction - start -end :math:`{} \times 2`

:math:`6 = 1 \times 3 \times 2`

In other words, the sheet is folded into three, then folded in half.

A sheet can be folded into three concertina wise, or using an envelope
fold. The pages end up in different orders depending on the folds made
and their order, and this needs to be taken into account during
imposition.


Signature Composition
--------------------------

As mentioned above, the size of a signature is governed by the number of
sheets it contains. A single sheet signature is :math:`2` pages with
duplex printing. The number of pages in a signature must be a multiple of
:math:`4`, considering the *fold*.
Therefore, permitted numbers of pages per signature are
:math:`4, 8, 16, 32, 64` and :math:`12, 24`.
:math:`12, 24` signatures have diffent folding processes from 
:math:`4, 8, 16, 32, 64`, as mentioned above.
Bigger sheets could be used :math:`>64` to make a single signature, but it
is not practical.


.. image:: ../_static/gathering_inserting.png

There are two types of methods to combine signatures, 
**inserting** and **gathering**. The signatures will look the same once
the edges are cut, but the order the pages are printed on the larger
sheet will differ depending on how they are folded.
The *gathering* does not affect to order of each signature but
*inserting* does to match the correct ordering of pages. 

The :math:`n` sheets signature is composed of :math:`i` time inserted
:math:`f` sheets signature.

.. math:: 
    n = i \times f.

If :math:`i = 1`, the signautre is complete itself. 

For example, :math:`16` sheets signature has next variation for same types.

* :math:`1 \times 16`
* :math:`2 \times 8`
* :math:`4 \times 4`

If we permit combinations of difference types.

* :math:`[4, 4, 8]`
* :math:`[4, 8, 4]`
* :math:`[8, 4, 4]`

Ordering of combinations in :math:`[,]` is important. The latter cases
are called **deep type** signature in book of T.B. Wiliams (1895).
With deep type, we can make every even number signature for example,

.. math::
    
    40 = 32 + 8 = 4 + 4+ 4+ ... +4 = 16 + 16 + 8, ...


Riffle direction
--------------------

.. image:: ../_static/riffle.png

**Riffle direction** is a direction of riffling (i.e. page turning) 
while reading the contents of a book.
It is dependant upon the reading direction of language. The most common
direction is a horizontal, from left top to right bottom (HLTRB).
There were various reading directions by the language system. While some
are no longer used, other reading directions are used more
frequently than one might think. 

Below are examples of languages with different reading directions.

* Asia, Korea, Japan, China ... etc 
    
    East Asians used a **VRTLB** (vertical, from right top to left
    bottom) system. 
    Nowadays, vertical writing is rarely seen in modern texts in Asia (it
    varies by country), but it is still used in design or a research works.
    For example, some Japanese manga use vertical writing in speech bubbles.
    Thgus speech bubbles are different shapes depending on the labguage.
    Japanese speech bubbles are vertically long while Korean ones are horizontally long. 
    Korea also used vertical writing histortically, but in the modern era it is
    not as popular as in Japan.
    This is an example of how the cultural difference, in this case writing
    direction, is visually expressed.

* Hebrew and Arabic 
    
    RL system

* Ancient Egyt 
    
    Their system was very special. They used both direction LR and RL. 
    The same characters can be written symmetrically by the direction.

* Elder Island script, Ogham scripts 
    
    These also have an abnormal direction, vertically from bottom to top.


Top to bottom, or bottom to top are not affected by the order of pages if
you riffle horizontally.
However, whether the reading direction is LR or RL the page ordering is 
affected considering reading efficiency.

The default setting of HornPenguin Booklet is a LR direction. *RL* is
also suppported.

Supporting *RL* is not complicated. Just reverse order the pages before
applying to rearrange transformation to the pages.


Printing markers
================================

Signature proof
-----------------

.. image:: ../_static/proof.png

**Signature proof** is a ordering proof marker on the spine of 
signatures. They ease the correct ordering of signatures
and make it easier to check if signatures are missing.


Crop marker
-----------------

Trim line indicator.


Registration marker
-----------------------

A **Registration marker** is added to check the registration of color
printing of printing machine.
Its color looks like the normal black color (CMYK(0, 0, 0, 1)) but 
actually, it is a special color called
*registration black*, CMYK code is (1, 1, 1, 0). If Cyan, Magenta
and Yellow are perfectly in proportion, the registration mark will
appear black.


Further reading
--------------------


* Matt T. Roberts and Don Etherington, Bookbinding and the Conservation
  of books: A Dictionary of Descriptive Terminology, Drawings by Margaret
  R. Brown

General and advanced information on bookbinding can be found in
the dictionary written by Matt T. Roberts and Don Etherington.
An `online version <https://cool.culturalheritage.org/don/>`_ is
available. 

* T.B. Wiliams, Hints on imposition. An illustrated guide for printer and
  pressman in the construction of book-forms, 1895. An `online version
  <https://archive.org/details/hintsonimpositio00will/mode/2up>` is available.
