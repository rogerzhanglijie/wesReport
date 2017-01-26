#-*-coding:utf-8-*-
#Author:Roger Zhang
#Date:2017-01-25
#Edition:Second
#Function: This script is used to convert the log parameters to pdf document format

from reportlab.lib.styles import getSampleStyleSheet 
from reportlab.rl_config import defaultPageSize 
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.units import inch,mm
from reportlab.lib.pagesizes import *
from reportlab.lib import colors 
from reportlab.platypus import *
import reportlab.rl_config
import ConfigParser
import datetime
import copy
import os
 

class wesReport:

	styles=''
	__Title=''
	__ReportName=''
	DefaultParagraphStyle=''
	__TitleFontSize=''
	__TitleFontName=''
	__PageNumFontSize=''
	__PageNumFontName=''
	__Config=''     #保存初始的config信息
	__LogoPath=''
	report_output_path=""
	exam_dict=''
	PAGE_HEIGHT= defaultPageSize[1]  
	PAGE_WIDTH=defaultPageSize[0] 
	def  __init__(self,config_path,exam_dict):
		self.__setDefaultParameter(config_path)
		self.exam_dict=exam_dict

	def __setDefaultParameter(self,config_path):
		config = ConfigParser.ConfigParser()
		config_path=os.path.join(config_path,"config.txt")
		config.read(config_path)
		#------------设置可应用的字体样式------------------#
		font_path=config.get("font","path")
		song=config.get("font","song")
		hei=config.get("font","hei")
		huawen=config.get("font","huawen")
		reportlab.rl_config.warnOnMissingFontGlyphs = 0
		pdfmetrics.registerFont(TTFont('song', os.path.join(font_path,song)))
		pdfmetrics.registerFont(TTFont('hei', os.path.join(font_path,hei)))
		pdfmetrics.registerFont(TTFont('huawen', os.path.join(font_path,huawen)))
		stylesheet= getSampleStyleSheet()
		styles= copy.deepcopy(stylesheet['Normal'])
		self.styles=styles
		self.__Config=config
		#------------设置报告常用参数-----------#
		self.__Title=config.get("report","Title")
		self.__ReportName=config.get("report","ReportName")
		#------------设置段落默认样式-----------#
		self.__setDefaultParagraphStyle(config)
		#------------设置Title的字体样式---------#
		self.__TitleFontSize=int(config.get("report","titleFontSize"))
		self.__TitleFontName=config.get("report","titleFontName")
		#-------------设置页码样式----------------#
		self.__PageNumFontSize=int(config.get("report","pageNumFontSize"))
		self.__PageNumFontName=config.get("report","pageNumFontName")
		#-------------设置logo的位置信息-----------#
		self.__LogoPath=config.get("report","logoPath")
		#--------------设置报告输出路径------------#
		self.report_output_path=config.get("report","reportPath")
	
	##############################设置默认段落样式######################################
	def __setDefaultParagraphStyle(self,config):
		stylesheet=getSampleStyleSheet()
		normalStyle = copy.deepcopy(stylesheet['Normal'])
		normalStyle.fontName=config.get("paragraph","fontName")
		normalStyle.leftIndent=int(config.get("paragraph","leftIndent"))
		normalStyle.splitLongWords=int(config.get("paragraph","splitLongWords"))
		normalStyle.spaceBefore=int(config.get("paragraph","spaceBefore"))
		normalStyle.borderWidth=int(config.get("paragraph","borderWidth"))
		normalStyle.borderPadding=int(config.get("paragraph","borderPadding"))
		normalStyle.fontSize=int(config.get("paragraph","fontSize"))
		normalStyle.leading=int(config.get("paragraph","leading"))
		self.DefaultParagraphStyle=normalStyle
		return self.DefaultParagraphStyle
	
	#########################设置标题###################################################
	def  __insertTitle(self,canvas,doc):
		canvas.saveState()
		canvas.setFont(self.__TitleFontName,self.__TitleFontSize)
		canvas.drawCentredString((self.PAGE_HEIGHT/2)+80, self.PAGE_HEIGHT-108, self.__Title)
		canvas.restoreState()
	
	#######################设置首页横线#################################################
	def __insertTwoHorizonLines(self,canvas,doc):
		# 设置线的颜色
		canvas.setStrokeColorRGB(0,0,0)
		# 绘制线
		#insert top line
		canvas.line(0.8*inch,9.5*inch,7.8*inch,9.5*inch) 
		#insert middle line
		canvas.line(0.8*inch,8.1*inch,7.8*inch,8.1*inch) 
		#insert Bottom Line
		canvas.line(0.8*inch,0.8*inch,7.8*inch,0.8*inch) 
		
	################################设置首页样式#########################################
	def myFirstPage(self,canvas,doc):
		self.__insertTitle(canvas,doc)
		canvas.saveState()   
		canvas.setFont('hei', 16)
		#insert top-bottom line
		self.__insertTwoHorizonLines(canvas,doc)
		#insert Report Name
		canvas.drawCentredString(self.PAGE_HEIGHT/2-100, self.PAGE_HEIGHT-150, self.__ReportName)
		#insert Clinical Test Data
		self.insertClinicalTest(canvas,doc)
		canvas.setFont(self.__PageNumFontName, self.__PageNumFontSize)
		canvas.drawString((self.PAGE_WIDTH/2)-20,10,u"1")   
		canvas.restoreState()
	
	def insertClinicalTest(self,canvas,doc):
		canvas.setFont('hei', 10)
		canvas.drawString(self.PAGE_HEIGHT/2-350, self.PAGE_HEIGHT-180, u"受检者信息")
		canvas.setFont('hei', 9)
		#first Line title
		canvas.drawString(self.PAGE_HEIGHT/2-350, self.PAGE_HEIGHT-200, u"受检者姓名：")
		canvas.drawString(self.PAGE_HEIGHT/2-240, self.PAGE_HEIGHT-200, u"样本标号：")
		canvas.drawString(self.PAGE_HEIGHT/2-130, self.PAGE_HEIGHT-200, u"性别：")
		canvas.drawString(self.PAGE_HEIGHT/2-10, self.PAGE_HEIGHT-200, u"年龄：")
		#second Line title
		canvas.drawString(self.PAGE_HEIGHT/2-350, self.PAGE_HEIGHT-220, u"样本类型：")
		canvas.drawString(self.PAGE_HEIGHT/2-240, self.PAGE_HEIGHT-220, u"送捡人：")
		canvas.drawString(self.PAGE_HEIGHT/2-130, self.PAGE_HEIGHT-220, u"送检日期：")
		canvas.drawString(self.PAGE_HEIGHT/2-10, self.PAGE_HEIGHT-220, u"报告日期：")
		#third Line title
		canvas.drawString(self.PAGE_HEIGHT/2-350, self.PAGE_HEIGHT-240, u"检测方法：")
		canvas.drawString(self.PAGE_HEIGHT/2-240, self.PAGE_HEIGHT-240, u"送捡单位：")
		
		canvas.setFont('song', 9)
		#first Line title Name
		canvas.drawString(self.PAGE_HEIGHT/2-290, self.PAGE_HEIGHT-200, self.exam_dict['name'])
		canvas.drawString(self.PAGE_HEIGHT/2-190, self.PAGE_HEIGHT-200, self.exam_dict['code'])
		canvas.drawString(self.PAGE_HEIGHT/2-100, self.PAGE_HEIGHT-200, self.exam_dict['sex'])
		canvas.drawString(self.PAGE_HEIGHT/2+20, self.PAGE_HEIGHT-200, self.exam_dict['age'])
		#second Line title Name
		canvas.drawString(self.PAGE_HEIGHT/2-300, self.PAGE_HEIGHT-220, self.exam_dict['sample_type'])
		canvas.drawString(self.PAGE_HEIGHT/2-200, self.PAGE_HEIGHT-220,self.exam_dict['send_people'])
		canvas.drawString(self.PAGE_HEIGHT/2-80, self.PAGE_HEIGHT-220, self.exam_dict['check_date'])
		
		if not exam_dict.has_key(""):
			self.exam_dict['report_date']=datetime.datetime.now().strftime('%Y-%m-%d')  
		
		canvas.drawString(self.PAGE_HEIGHT/2+40, self.PAGE_HEIGHT-220, self.exam_dict['report_date'])
		#third Line title Name
		canvas.drawString(self.PAGE_HEIGHT/2-300, self.PAGE_HEIGHT-240,self.exam_dict['check_method'])
		canvas.drawString(self.PAGE_HEIGHT/2-190, self.PAGE_HEIGHT-240, self.exam_dict['unit'])
		#clinical log
		canvas.setFont('hei', 10)
		canvas.drawString(self.PAGE_HEIGHT/2-350, self.PAGE_HEIGHT-280, u"临床信息")
		canvas.setFont('song', 9)
	
	def insertClinicalAnnotation(self):
		normalStyle=self.DefaultParagraphStyle
		para=Paragraph(self.exam_dict['annotation'], normalStyle)
		return para 
		
	def myLaterPages(self,canvas, doc):  
		insertTitle(canvas,doc)
		canvas.saveState()
		canvas.setFont(self.__PageNumFontName, self.__PageNumFontSize)
		canvas.drawString((self.PAGE_WIDTH/2)-20,10,u"%d" % (doc.page))
		canvas.restoreState()
	
	def insertPageLogo(self):
		I=Image(self.__LogoPath)
		I.hAlign="LEFT"
		I.drawHeight = 2*inch*I.drawHeight / I.drawWidth
		I.drawWidth = 2*inch
		return I
	
	def renderPDF(self,report_name):
		Story=[]
		report_path=os.path.join(self.report_output_path,report_name)
		doc = SimpleDocTemplate(report_path,pagesize=A4) 
		logo=self.insertPageLogo()
		Story.append(logo)
		Story.append(Spacer(1, 2.2*inch))
		Story.append(self.insertClinicalAnnotation())
		Story.append(PageBreak())
		doc.build(Story,onFirstPage=self.myFirstPage,onLaterPages=self.myLaterPages)
		
if   __name__=="__main__":
	exam_dict={'name':u'王昆','code':u'6E013','sex':u'男','age':u'45','sample_type':u'外周血','send_people':u'何蓉','check_date':u'2016-09-26','check_method':u'WES检测','unit':u'中国医科大学附属盛京医院','annotation':u'的刷卡积分哈就开始放假咯是否喝酒撒'}
	s=wesReport("./",exam_dict)
	print s.PAGE_HEIGHT
	print s.PAGE_WIDTH
	s.renderPDF("test.pdf")