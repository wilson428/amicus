from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter, process_pdf
from pdfminer.converter import TextConverter, HTMLConverter

rsrcmgr = PDFResourceManager()

def convert(fname, outfile):
    fp = file(fname, 'rb')
    #text
    outfp = file(outfile + ".txt", 'w')
    device = TextConverter(rsrcmgr, outfp, codec='utf-8')
    process_pdf(rsrcmgr, device, fp)
    outfp.close()
    
    '''
    #html    
    outfp = file(outfile + ".html", 'w')
    device = HTMLConverter(rsrcmgr, outfp, codec='utf-8')
    process_pdf(rsrcmgr, device, fp)
    outfp.close()
    '''
    
    fp.close()
