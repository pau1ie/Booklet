from __future__ import annotations
import re

import PyPDF2 as pypdf
import webbrowser
from datetime import datetime
import textdata
import sys, os, math, io, tempfile

from itertools import permutations

from svglib.svglib import svg2rlg
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib.colors import CMYKColor, CMYKColorSep
from reportlab.graphics.shapes import *

import numpy as np


color_black = CMYKColor(0, 0, 0, 1)
color_cyan = CMYKColor(1, 0, 0, 0)
color_magenta = CMYKColor(0, 1, 0, 0)
color_yellow = CMYKColor(0, 0, 1, 0)

registration_black = CMYKColor(1,1,1,1)


# System directory
def resource_path(relative_path, directory):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, directory, relative_path)


#Utils===============================================================================
pts_to_mm = mm
def pts_mm(size:tuple, mode=True):
    if mode: #pts to mm
        x = round(size[0]/pts_to_mm,0)
        y = round(size[1]/pts_to_mm,0)
        return (x,y)
    else:   #mm to pts
        x = size[0] * pts_to_mm
        y = size[1] * pts_to_mm
        return (x,y)

def open_url(url):
        return webbrowser.open(url)

def split_list(li:list, n:int)->list: #n: length of sub list
    if len(li) %n !=0:
        raise ValueError(f"The length of sublist, {n}, must be a divider of original list, {len(li)}. ")
    
    rlist =[]
    for i in range(0, int(len(li)/n)):
        ni = n*i
        rlist.append([li[ni: ni+n]][0])

    return rlist

def convert(hex:str)->tuple:
    if "#" in hex:
        hex= hex.replace("#","")
    R, G, B  = int(hex[0:2],16), int(hex[2:4],16), int(hex[4:6],16)
    
    R = R/255
    G = G/255
    B = B/255

    K = 1- max(R,G,B)
    C = (1-R-K)/(1 - K)
    M = (1-G-K)/(1 - K)
    Y = (1-B-K)/(1 - K)
    return C, M, Y, K

#Permutations and generating functions for signature routines-------------------------
class Permutation:
    @classmethod
    def get_permutations(cls, n, per=False): # get list of permutations for given 'n'
        per = permutations(range(1, n+1), n)
        if per:
            return [cls(n, p) for p in per]
        else:
            return [ p for p in per]
    @classmethod
    def reverse_permutation(cls, n):
        return cls(n, range(n, 0, -1)) 


    def __init__(self, n, plist):
        if len(plist) != n:
            raise ValueError(f"{n} must be same with len(plist) = {len(plist)}")

        if sum(plist) != int(n* (n+1)/2):
            raise ValueError(f"plist does not satisfy permutation proeprty.\n All [0, n-1] values must be in plist. \n {plist}")

        self.n = n
        self.plist = plist
    def __getitem__(self, key):
        if type(key) != int:
            raise ValueError(f"key must be an integer type element: {key}")
        if key < 1 or key > self.n:
            raise IndexError(f"{key} must be in [1, {self.n}] range.")
        
        return self.plist[key-1]
    def __mul__(self, other: Permutation) -> Permutation:
        if self.n != other.n:
            raise ValueError(f"{self.n} and {other.n} are not same.")
        
        rlist = [other[x] for x in self.plist]
        return Permutation(self.n, rlist)

    def index_mul(self, other, oper=False):

        rlist = [self[x] for x in other.plist]
        if oper:
            self.plist= rlist
        else:
            return Permutation(self.n, rlist)

    def index_mul_partial(self, sub_permutation, oper = False): #Work on indexing
        if not isinstance( sub_permutation, Permutation):
            raise ValueError(f"Given parameter must be \'Permutation\' object. \n Current object:{type(sub_permutation)}")
        if self.n %sub_permutation.n != 0:
            raise ValueError(f"Sub permutation must have a divisor of main permuatain size as its size\n main:{self.n}, sub:{sub_permutation.n}")

        n = int(self.n / sub_permutation.n)
        m = sub_permutation.n
        
        rlist = []
        for i in range(0,n):
            tem_rlist = [self.plist[x+m*i -1] for x in sub_permutation.plist]
            rlist = rlist + tem_rlist
        
        if oper:
            self.plist = rlist
        else:
            return Permutation(self.n, rlist)

    def permute_to_list_index(self, li):
        if len(li) != self.n:
            raise ValueError(f"{len(li)} ! = {self.n}")
        
        rlist = [li[x-1] for x in self.plist ]
        return rlist

    def inverse(self)-> Permutation:
        ilist= [self.plist.index(x)+1 for x in range(1, self.n+1)]
        return Permutation(self.n, ilist)
    
    def notation_cauchy(self):
        return f"{list(range(1, self.n+1))}\n{self.plist}"

    
    def __canocial_order(self, cyclist):
        c_clist_1 = []
        c_clist_2 = []
        for li in cyclist:
            n = len(li)
            nmax = li.index(max(li))
            c_clist_1.append([li[x] for x in range(nmax-n, nmax)])
        maxindex = [x[0] for x in c_clist_1]
        s_index = sorted(maxindex)

        for i in s_index:
            c_clist_2.append(c_clist_1[maxindex.index(i)])
        
        return c_clist_2

    def notation_cyclic(self, canonical=False, string= False, sep=''):
        cycliclist = []
        index = list(range(1, self.n+1))
        i =1

        while True:
            ilist = []
            ilist.append(i)
            index.remove(i)
            
            sig_i = self[i]
            while sig_i in index:
                ilist.append(sig_i)
                index.remove(sig_i)
                sig_i = self[sig_i]
            
            cycliclist.append(ilist)

            if len(index) > 0:
                i = min(index)
            else: 
                break
        if canonical:
            cycliclist = self.__canocial_order(cycliclist)
        
        if string:
            cycstr = ''
            for li in cycliclist:
                cycstr = cycstr+ '('+f'{sep}'.join(map(str,li))+')'
            return cycstr
        else:
            return cycliclist


#PDF Utils=================================================================================

class PDFsig:
    _fold_arrange = {
        4: [
            [4,1],
            [2,3]
        ],
        8: [
            [8,1,5,4],
            [2,7,3,9]
        ],
        12: [
            [12,1,9,4,8,5],
            [2,11,3,10,6,7]
        ],
        16: [
            [16,1,4,13,9,8,5,12],
            [10,7,6,11,15,2,3,14]
        ],
        24: [
            [24, 1, 12, 13, 21, 4, 9, 16, 20, 5, 8, 17],
            [14, 11, 2, 23, 15, 10, 3, 22, 18, 7, 6, 19]
        ],
        32: [
            [44,21,28,37,40,25,24,41,53,12,5,60,57,8,9,56,52,13,4,61,64,1,16,49,45,20,29,36,33,32,17,48],
            [46,19,30,35,34,31,18,47,51,14,3,62,63,2,15,50,54,11,6,59,58,7,10,55,43,22,27,38,39,26,23,42]
        ]
    }

    def __fold_matrix_update(self, n, matrix):
        n_1 = np.flip(matrix.T, axis=0)
        len_n = len(n_1[0])
        l = int(len_n/2)

        rows =[]
        for row in n_1:
            r_split = np.split(row,l)
            row_appended = []

            for tu in r_split:
                tem = np.array([n-tu[0] +1,n-tu[1] +1])
                row_appended.append(np.insert(tem, 1, tu))    
            rows.append(np.concatenate(row_appended, axis=None))     
        return np.stack(rows)

    @staticmethod
    def get_info(path:str) -> tuple:
        pdf = pypdf.PdfFileReader(path)

        page_num = pdf.getNumPages()

        if page_num != 0:
            pdfinfo = pdf.metadata

            title = pdfinfo['/Title'] if '/Title' in pdfinfo.keys() else 'None'
            authors = pdfinfo['/Author'] if '/Author' in pdfinfo.keys() else 'Unkown'
            page_size=  pdf.getPage(0).mediaBox[2:]
            page_size[0] = float(page_size[0]) 
            page_size[1] = float(page_size[1]) 
            return title, authors, page_num, page_size
        
        return False, False, False, False
    @staticmethod
    def sig_layout(n:int) -> tuple:
        if type(n) != int or n<4 or n%4 !=0:
            raise ValueError(f"n:{n} must be a positive integer that multiple of 4.")

        if n%3 ==0:
            i = math.log2(n) - math.log2(3) -1
            return(3, int(2**i))
        else:
            i = int(math.log2(n/4))
            if i%2 :
                k = kp = int((i+1)/2)
            else:
                k = int(i/2)
                kp = k+1
            return (int(2**k), int(2**kp))
    @classmethod
    def fold_arrange_n(cls,n: int) -> list:
        if n % 4 !=0:
            raise ValueError("Fold sheets must be 4*2^k for k= 0, 1, 2, .... \n Current value is {n}")
    
        if n <64:
            return cls._fold_arrange[n]
        else:
            n_iter = int(math.log(n/16,2))
            n_i = 32
            per_n_1 = [cls._fold_arrange[n_i][0], cls._fold_arrange[n_i][1]]
    
            #permutation to matrix
            layout_n_1 = cls.sig_layout(n_i)
            front_matrix = np.array(per_n_1[0]).reshape(layout_n_1)
            back_matrix = np.array(per_n_1[1]).reshape(layout_n_1)
            for i in range(0, n_iter):
                n_i = 2*n_i
                front_matrix = cls.__fold_matrix_update(n_i, front_matrix)
                back_matrix = cls.__fold_matrix_update(n_i, back_matrix)   
        per_fn = np.concatenate(front_matrix).tolist() 
        per_bn = np.concatenate(back_matrix).tolist()
    
        return [per_fn, per_bn]       
    @classmethod
    def fold_list_n(cls, n, per=False):
        if n % 4 !=0:
            raise ValueError("Fold sheets must be 4*2^k for k= 0, 1, 2, .... \n Current value is {n}")
        
        if n < 64:
            return cls._fold_arrange[n]
        else:
            n_iter = int(math.log(n/16,2))
            n_i = 32
            per_n_1 = [cls._fold_arrange[n_i][0], cls._fold_arrange[n_i][1]]

            #permutation to matrix
            layout_n_1 = cls.sig_layout(n_i)
            front_matrix = np.array(per_n_1[0]).reshape(layout_n_1)
            back_matrix = np.array(per_n_1[1]).reshape(layout_n_1)
            for i in range(0, n_iter):
                n_i = 2*n_i
                front_matrix = cls.__fold_matrix_update(n_i, front_matrix)
                back_matrix = cls.__fold_matrix_update(n_i, back_matrix)   
        per_fn = np.concatenate(front_matrix).tolist() 
        per_bn = np.concatenate(back_matrix).tolist()

        if per:
            Permutation(n, per_fn+per_bn )
        else:
            return [per_fn, per_bn]      
    @classmethod
    def sig_rearrange(cls, nn, ns): #1
        n_l = nn*ns

        nlist = [i+1 for i in range(0, n_l)]
        nlist_splited = split_list(nlist, int(ns/2))
        rlist=[]

        n_splited = 2*nn
        for i in range(0,nn):
            rlist = rlist + nlist_splited[i] + nlist_splited[n_splited-i-1]

        return rlist
    @classmethod
    def signature_permutation(cls, n, nn, ns, riffle=True):
        permutation_riffle = Permutation(n, range(1, n+1)) if riffle else  Permutation.reverse_permutation(n)
        permutation_signature = Permutation(n, cls.sig_rearrange(nn,ns)).index_mul_partial(cls.fold_list_n(ns, per=True))

        return permutation_riffle * permutation_signature
    @classmethod
    def get_page_range(cls, pagerange:str):

        pagerange = pagerange.replace(" ","")
        rlist=  []
        for st in pagerange.split(","):
            if '-' in st:
                i, l = st.split("-")
                i = int(i)
                l = int(l)
                r = l-i+1

                rlist = rlist +[i + d for d in range(0,r)]
            else:
                rlist.append(int(st))
            
            return rlist

    @classmethod
    def generate_layout(#All dimensions are written in pts unit
        cls,
        pagesize:tuple, 
        pagenum:int,
        n:tuple, nd:int, d:int, 
        proof:bool, proofcode:str, 
        trim:bool, 
        registration:bool, 
        cmyk:bool
    ):

        #Signature composition
        ni = n[0]
        ns = n[1]

        n_block = int(pagenum/(ni * ns))

        
        #Paper Dimension
        arrange = cls.sig_layout(ns)
        ny = arrange[0]
        nx = arrange[1]
        x = 2*nd + nx*pagesize[0] + (nx-1)*d    
        y = 2*nd + ny*pagesize[1] + (ny-1)*d

        #Signature proof
        if proof:
            proof_height = pagesize[1]/n_block
            proof_width = d
            cmyk_proof = convert(proofcode)
            proof_position = [nd+pagesize[0], nd+ny*pagesize[1] + (ny-1)*d-proof_height]
        #trim
        if trim:
            trim_l = nd*(1/2)
            #horizontal line
            x1 = nd/4
            x2 = nd + nx*pagesize[0] + (nx-1)*d +x1
            y1 = nd + ny*pagesize[1] + (ny-1)*d
            y2 = nd
            #vertical line
            x3 = nd
            x4 = x2 - x1
            y3 = nd/4
            y4 = y1 + y3

            trim_lines = [
                (x1,y1, x1 + trim_l, y1), # h, u l
                (x1,y2, x1 + trim_l, y2), # h, d l
                (x2,y1, x2 + trim_l, y1), # h, u r
                (x2,y2, x2 + trim_l, y2), # h, d r
                (x3,y4, x3, y4 + trim_l), # v, u l
                (x3,y3, x3, y3 + trim_l), # v, d l
                (x4,y4, x4, y4 + trim_l), # v, u r
                (x4,y3, x4, y3 + trim_l)  # v, d r
            ]
        if registration:
            l = (4/5) * nd
            dis = nd/2

            if not trim:
                #horizontal line
                x1 = nd/4
                x2 = nd + nx*pagesize[0] + (nx-1)*d +x1
                y1 = nd + ny*pagesize[1] + (ny-1)*d
                y2 = nd
                #vertical line
                x3 = nd
                x4 = x2 - x1
                y3 = nd/4
                y4 = y1 + y3
            regist_coords =[
                (dis - l/2, y1-dis - l),
                (dis - l/2, y2 + dis),
                (x2 + trim_l/2 - l/2, y1-dis - l),
                (x2 + trim_l/2 - l/2, y2 + dis),
                (x3 + dis, y4+trim_l/2 - l/2),
                (x3 + dis, dis - l/2),
                (x4 - dis -l, y4+trim_l/2 - l/2),
                (x4 - dis -l, dis - l/2),
            ]
        if cmyk:
            rec_l = nd/2
            rec_d = nd/8
            cmyk_position = [nd/4, y1-rec_l*2]

        tem_pdf_byte = io.BytesIO()

        layout = canvas.Canvas(tem_pdf_byte, pagesize = (x,y))

        for i in range(0, n_block):
            for j in range(0, ni):

                #fill basic layout components
                if proof and j==0 : # draw rectangle
                    layout.setLineWidth(0)
                    layout.setFillColorCMYK(cmyk_proof[0], cmyk_proof[1] ,cmyk_proof[2], cmyk_proof[3])
                    layout.rect(proof_position[0], proof_position[1], proof_width, proof_height, fill=1)

                    proof_position[1] = proof_position[1] - proof_height
                for k in range(0,2):  
                    if trim: # draw line
                        layout.setLineWidth(0.5*mm)
                        layout.lines(trim_lines)
                    if registration: # add image
                        cls._drawRegistrationMark(layout, regist_coords[0][0], regist_coords[0][1], l)
                        cls._drawRegistrationMark(layout, regist_coords[1][0], regist_coords[1][1], l)
                        cls._drawRegistrationMark(layout, regist_coords[2][0], regist_coords[2][1], l)
                        cls._drawRegistrationMark(layout, regist_coords[3][0], regist_coords[3][1], l)
                        cls._drawRegistrationMark(layout, regist_coords[4][0], regist_coords[4][1], l)
                        cls._drawRegistrationMark(layout, regist_coords[5][0], regist_coords[5][1], l)
                        cls._drawRegistrationMark(layout, regist_coords[6][0], regist_coords[6][1], l)
                        cls._drawRegistrationMark(layout, regist_coords[7][0], regist_coords[7][1], l)
                    if cmyk: 
                        layout.setLineWidth(0)
                        layout.setFillColor(color_cyan)
                        layout.rect(cmyk_position[0], cmyk_position[1], rec_l, rec_l, fill=1)
                        cmyk_position[1] -=(rec_d + rec_l)
                        layout.setFillColor(color_magenta)
                        layout.rect(cmyk_position[0], cmyk_position[1], rec_l, rec_l, fill=1)
                        cmyk_position[1] -=(rec_d + rec_l)
                        layout.setFillColor(color_yellow)
                        layout.rect(cmyk_position[0], cmyk_position[1], rec_l, rec_l, fill=1)
                        cmyk_position[1] -=(rec_d + rec_l)
                        layout.setFillColor(color_black)
                        layout.rect(cmyk_position[0], cmyk_position[1], rec_l, rec_l, fill=1)
                        cmyk_position[1] = y1-rec_l*2


                    layout.showPage()

        #----------------------------
        layout.save()
        tem_pdf_byte.seek(0)
        tem_pdf  = pypdf.PdfReader(tem_pdf_byte)
        return tem_pdf, tem_pdf_byte

    def _drawRegistrationMark(self, canvas, x, y, l):

        def get_abpath4(x0,y0,x1, y1):
            return (x+x0, y+y0, x+x1, y+y1)

        def get_abpath2(x0,y0):
            return x+x0, y+y0

        line_t = l/15 #/25
        line_l = l*(3/16)
        circle_r1 = l*(5/16) - line_t
        circle_r2 = circle_r1 - line_t*(1.5)

        lines = [
            get_abpath4(0,l/2, line_l, l/2),
            get_abpath4(l-line_l, l/2, l,l/2),
            get_abpath4(l/2,0, l/2, line_l),
            get_abpath4(l/2,l-line_l,l/2,l)
        ]

        canvas.setLineWidth(line_t)
        canvas.setStrokeColor(registration_black)
        canvas.setFillColor(registration_black)
        #lines
        canvas.lines(lines)

        #outter
        arcs = canvas.beginPath()
        #arcs.circle(x+l/2+line_t, y+l/2+line_t, circle_r1)
        c = l/2 - line_t/2
        #x1 = c - circle_r1
        #x2 = c + circle_r1
        #x1, x2 = get_abpath2(x1, x2)
        #arcs.circle(x+ c, y+c , circle_r1)
        x1 = c- circle_r1
        x2 = c+ circle_r1
        #상대 경로는 같아도 절대 경로에서는 x,y값이 같지 않음
        x1, y1 = get_abpath2(x1, x1)
        x2, y2 = get_abpath2(x2, x2)
        arcs.arc(x1,        y1,         x2,         y2,         startAng=180,   extent=90)
        arcs.arc(x1+line_t, y1,         x2+line_t,  y2,         startAng=270,   extent=90)
        arcs.arc(x1+line_t, y1+line_t,  x2+line_t,  y2+line_t,  startAng=0,     extent=90)
        arcs.arc(x1,        y1+line_t,  x2,         y2+line_t,  startAng=90,   extent=90)
        canvas.drawPath(arcs, fill=0, stroke=1)

        #inner
        arcs_fill = canvas.beginPath()
        #arcs_fill.circle(x+l/2, y+l/2, circle_r2)
        x1 = c - circle_r2
        x2 = c + circle_r2
        x1, y1 = get_abpath2(x1, x1)
        x2, y2 = get_abpath2(x2, x2)

        xc , yc = get_abpath2(l/2, l/2)

        d= line_t/2

        arcs_fill.moveTo(xc-d, yc-d)
        arcs_fill.arcTo(x1,        y1,         x2,         y2,         startAng=180,   extent=90)
        

        arcs_fill.moveTo(xc +d, yc-d)
        arcs_fill.arcTo(x1+line_t, y1,         x2+line_t,  y2,         startAng=270,   extent=90)
        

        arcs_fill.moveTo(xc +d, yc +d)
        arcs_fill.arcTo(x1+line_t, y1+line_t,  x2+line_t,  y2+line_t,  startAng=0,     extent=90)
        
        
        arcs_fill.moveTo(xc -d, yc +d)
        arcs_fill.arcTo(x1,        y1+line_t,  x2,         y2+line_t,  startAng=90,    extent=90)
        
        canvas.drawPath(arcs_fill, fill=1, stroke=0)

        return 0

    def generate_signature(
                            self,
                            inputfile:str,
                            outputfile:str,
                            pagerange:str,
                            leaves:list,
                            fold:bool,
                            riffle:bool,
                            format:list,
                            imposition:bool,
                            blank:list,
                            split:bool,
                            sigproof:list, #Printing marks
                            trim:bool,
                            registration:bool,
                            cmyk:bool
        ):
        #Parameters
        # 1. filename(str): File name of output
        # 1. leaves(list(nl, nn, ns)) 
        #               nl(int): number of leaves per signature
        #               nn(int): number of sub signature
        #               ns(int): number of leaves per subsignature: nl = nn x ns
        # 2. fold(bool): determines n-fold book or not( fold more than 1 per each papaer)
        # 3. riffle(bool): determines reiffle direction of pages, default = False(left to right)
        # 4. format(list(formatbool, width, height)): paper format dimension
        # 5. imposition(bool):
        # 6. blank(list(mode, n))
        #               mode(str): determines distribution of additional blank page to its value(front, back, both(=equal)).
        #               n(int): number of additional blank page(s).
        # 7. split(bool): determines whether split each signatures as disfferent files or not.
        # 8. sigproof(list(sigproofbool sig_color)) 
        #               sigproofbool(bool): determines add sigproof or not
        #               sig_color: hex color code
        # 9. trim(bool): add trim or not
        # 10. registration(bool): add registration or not
        # 11. cymk(bool): add cymk proof or not  

        if imposition:
            fold = True

        manuscript_pdf = pypdf.PdfFileReader(str(inputfile))
        output_pdf = pypdf.PdfFileWriter()

        #Copy meta datas and add modificaion 'date' and 'producer'
        # PyPDF@ has an error for directly put PdfReader class meta to PdfWriter calss'
        # We have to convert them with string variable.

        meta = {}
        for key in manuscript_pdf.metadata.keys():
            val = manuscript_pdf.metadata.raw_get(key)
            meta[key] = str(val) #converting to string
        
        output_pdf.addmetadata(meta)
        output_pdf.addmetadata({"/Producer": "HornPenguin Booklet"})
        output_pdf.addmetadata({"/ModDate": f"{datetime.now()}"})

        #Calculate page range
        page_range = self.cal_page_range(pagerange) #Implementation is needed
        
        #Blank pages
        blankmode = blank[0]
        blanknum = blank[1]
        if blankmode == "fonrt":
            blankfront = blanknum
        elif blankmode == "both":
            blankfront = int(blanknum/2)
        else:
            blankfront = 0

        blankback = blanknum - blankfront

        blankfront_list = [0 for i in range(0, blankfront)] 
        blankback_list  = [0 for i in range(0, blankback)]
        page_range = blankfront_list + page_range +blankback_list


        #Get permutation of given range and signature.
        nl = leaves[0]
        nn = leaves[1]
        ns = leaves[2]
        sig_permutation = self.signature_permutation(nn, ns, riffle=riffle)

        #Format scale
        if format[0]:

            pPage_width, pPage_height = pts_mm(format[1], format[2], False)
            f_dim = textdata.PaperFormat[format[3]].split("x")
            pFormat_width, pFormat_height  = pts_mm(int(f_dim[0]), int(f_dim[1]), False)

            scale_x = pFormat_width  / pPage_width 
            scale_y = pFormat_height / pPage_height 

        else:
            scale_x = scale_y = 1.0

        
        #-----------------------------------------------------------------------
        pro_blocks = split_list(page_range, nl)

        if fold:
            #layout = self.generate_layout()
            for block in pro_blocks:
                per_block  = sig_permutation.permute_to_list_index(block)
                foldlist = split_list(per_block, 2*nl)[1::2]
                for i in per_block:
                    if i==0:
                        output_pdf.add_blank_page(width = pFormat_width, height = pFormat_height)
                    else:
                        page = manuscript_pdf.pages[i] if i in foldlist else manuscript_pdf.pages[i].rotate_clockwise(180)
                        page.scale(scale_x, scale_y)
                        output_pdf.add_page(manuscript_pdf.pages[i])
        else:
            for block in pro_blocks:
                per_block  = sig_permutation.permute_to_list_index(block)
                for i in per_block:
                    if i==0:
                        output_pdf.add_blank_page(width = pFormat_width, height = pFormat_height)
                    else:
                        page = manuscript_pdf.pages[i]
                        page.scale(scale_x, scale_y)
                        output_pdf.add_page(manuscript_pdf.pages[i])

            

        #------------------------------------------------------------------------
        # Todo: using reportlab library generate temper pdf file for printing marks
        # 
        
        ndbool = trim or registration or cmyk
        printbool = sigproof[0] or ndbool
        
        nd = 40 if ndbool else 0

        if imposition or printbool:
            if imposition:
                composition = (nn,ns)
            else:
                composition = (1,1)
        
            tem_pdf, temfile = self.generate_layout(
                    (pFormat_width, pFormat_height),
                    len(page_range),
                    composition,
                    nd = nd,
                    d =5,
                    proof = sigproof[0],
                    proofcode= sigproof[1],
                    trim = trim,
                    registration=registration,
                    cmyk = cmyk
            )

            layout = self.sig_layout(ns) if composition[0] != 1 else (1,1)

            def position(i, layout):
                nx = layout[0]
                ny = layout[1]
                r = i % nx
            for i in range(0,len(tem_pdf.pages)):
                page = tem_pdf.pages[i]
                for 
                    page.merge_page()

        else:
            #Save files
            with open(outputfile, "wb") as f:
                output_pdf.write(f)
