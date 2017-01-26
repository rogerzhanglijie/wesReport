#coding=utf-8

#测试数据内容
def init_config():
    import reportlab.rl_config
    reportlab.rl_config.warnOnMissingFontGlyphs = 0
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    import copy
    pdfmetrics.registerFont(TTFont('song', 'font/SURSONG.TTF'))
    stylesheet= getSampleStyleSheet()
    styles= copy.deepcopy(stylesheet['Normal'])
    styles.fontName ='song'
    styles.fontSize = 20
    return styles
from reportlab.platypus import *
from reportlab.lib.styles import getSampleStyleSheet   
from reportlab.rl_config import defaultPageSize   
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import *
#from reportlab.lib.utils import *
from reportlab.lib.units import mm
styles=init_config() 
PAGE_HEIGHT=defaultPageSize[1]   
PAGE_WIDTH=defaultPageSize[0]
Title = "Hello world"  
pageinfo = "platypus example"  
def myFirstPage(canvas,doc):   
    canvas.saveState()   
    canvas.setFont('song',16)   
    canvas.drawCentredString(PAGE_HEIGHT/2, PAGE_HEIGHT-108, Title)   
    canvas.setFont('song',9)   
    canvas.drawString((PAGE_WIDTH/2)-20,10,u"首页")   
    canvas.restoreState() 
def myLaterPages(canvas, doc):   
    canvas.saveState()   
    canvas.setFont('song', 9)   
    canvas.drawString((PAGE_WIDTH/2)-20,10,u"页码:%d 页" % (doc.page))   
    canvas.restoreState()
def Go():   
    doc = SimpleDocTemplate("phello.pdf",pagesize=A4)  
    #Story = [Spacer(1,2*inch)]   
    #style = styles["Normal"]
    i=0
    I=Image("logo.jpg")
    I.drawHeight = 1*inch*I.drawHeight / I.drawWidth
    I.drawWidth = 1*inch
    print str(doc.allowSplitting)+"adsfasfasd"
    Story=[]
    for i in range(10):
        Story.append(I)
        Story.append(PageBreak())
    #doc.build(Story)
    doc.build(Story, onFirstPage=myFirstPage, onLaterPages=myLaterPages)
    '''for i in range(100):
        I = Image("logo.jpg")
        #print dir(I)
        #vl=getImageData('logo.jpg')
        #print vl
        #I.drawWidth=
        #I.drawHeight=str(I.imageHeight)+'px'
        bogustext=(u"测试数字：%s."%i)
        p = Paragraph(bogustext, styles)   
        Story.append(p)
        Story.append(I)
        Story.append(Spacer(1,0.2*inch))   
        doc.build(Story, onFirstPage=myFirstPage, onLaterPages=myLaterPages)
        print i'''
if __name__ == "__main__":
   # init_config()
    Go()  