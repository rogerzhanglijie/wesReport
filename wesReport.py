#-*-coding:utf-8-*-
#Author:Roger Zhang
#Date:2017-01-25
#Edition:Second
#Function: This script is used to convert the log parameters to pdf document format

from reportlab.lib.styles import getSampleStyleSheet 
from reportlab.rl_config import defaultPageSize 
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.units import inch,cm,mm
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
	__ParaDelimiter=""  #段落分隔符
	report_output_path=""
	exam_dict=''
	__ExamineSignature=""
	__CheckSignature=""
	__HorizonTopImagePath=""
	__HorizonBottomImagePath=""
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
		#--------------设置段落分隔符--------------#
		self.__ParaDelimiter=config.get("paragraph","paraDelimiter")
		#--------------设置签名路径----------------#
		self.__ExamineSignature=config.get("signature","examineSignature")
		self.__CheckSignature=config.get("signature","checkSignature")
		#--------------水平横线图路径--------------#
		self.__HorizonTopImagePath=config.get("report","horizonTopImagePath")
		self.__HorizonBottomImagePath=config.get("report","horizonBottomImagePath")
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
		canvas.drawCentredString((self.PAGE_WIDTH/2)+430, self.PAGE_WIDTH-90, self.__Title)
		canvas.restoreState()
	
	#######################设置首页横线#################################################
	def __insertTwoHorizonLines(self,canvas,doc):
		# 设置线的颜色  
		canvas.setStrokeColorRGB(0,0,0)
		# 绘制线
		#insert top line
		canvas.line(1.2*inch,6.5*inch,10.9*inch,6.5*inch) 
		#insert middle line
		canvas.line(1.2*inch,5.2*inch,10.9*inch,5.2*inch)
		#insert Bottom Line
		canvas.line(1.2*inch,1.2*inch,10.9*inch,1.2*inch) 
		
	################################设置首页样式#########################################
	def myFirstPage(self,canvas,doc):
		self.__insertTitle(canvas,doc)
		canvas.saveState()  
		I=Image(self.__LogoPath)
		I.hAlign="LEFT"
		I.drawWidth=3*inch
		drawHeight = 3*inch*I.drawHeight / I.drawWidth-0.5*inch
		drawWidth = 3*inch
		canvas.drawInlineImage(self.__LogoPath,0.8*inch,6.7*inch,drawWidth,drawHeight)		
		canvas.setFont('hei', 20)
		#insert top-bottom line
		self.__insertTwoHorizonLines(canvas,doc)
		#insert Report Name
		canvas.drawCentredString((self.PAGE_WIDTH/2)+150, self.PAGE_WIDTH-120, self.__ReportName)
		#insert Clinical Test Data
		self.insertClinicalTest(canvas,doc)
		canvas.setFont(self.__PageNumFontName, self.__PageNumFontSize)
		canvas.drawString((self.PAGE_WIDTH/2)+150,50,u"1")   
		canvas.restoreState()
	
	def insertClinicalTest(self,canvas,doc):
		canvas.setFont('hei', 13)
		canvas.drawString(self.PAGE_WIDTH/2-200, self.PAGE_WIDTH-150, u"受检者信息")
		canvas.setFont('hei', 11)
		#first Line title
		canvas.drawString(self.PAGE_WIDTH/2-200, self.PAGE_WIDTH-170, u"受检者姓名：")
		canvas.drawString(self.PAGE_WIDTH/2-30, self.PAGE_WIDTH-170, u"样本标号：")
		canvas.drawString(self.PAGE_WIDTH/2+110, self.PAGE_WIDTH-170, u"性别：")
		canvas.drawString(self.PAGE_WIDTH/2+250, self.PAGE_WIDTH-170, u"年龄：")
		#second Line title
		canvas.drawString(self.PAGE_WIDTH/2-200, self.PAGE_WIDTH-190, u"样本类型：")
		canvas.drawString(self.PAGE_WIDTH/2-30, self.PAGE_WIDTH-190, u"送捡人：")
		canvas.drawString(self.PAGE_WIDTH/2+110, self.PAGE_WIDTH-190, u"送检日期：")
		canvas.drawString(self.PAGE_WIDTH/2+250, self.PAGE_WIDTH-190, u"报告日期：")
		#third Line title
		canvas.drawString(self.PAGE_WIDTH/2-200, self.PAGE_WIDTH-210, u"检测方法：")
		canvas.drawString(self.PAGE_WIDTH/2-30, self.PAGE_WIDTH-210, u"送捡单位：")
		
		canvas.setFont('song', 11)
		#first Line title Name
		canvas.drawString(self.PAGE_WIDTH/2-130, self.PAGE_WIDTH-170, self.exam_dict['name'])
		canvas.drawString(self.PAGE_WIDTH/2+30, self.PAGE_WIDTH-170, self.exam_dict['code'])
		canvas.drawString(self.PAGE_WIDTH/2+150, self.PAGE_WIDTH-170, self.exam_dict['sex'])
		canvas.drawString(self.PAGE_WIDTH/2+280, self.PAGE_WIDTH-170, self.exam_dict['age'])
		#second Line title Name
		canvas.drawString(self.PAGE_WIDTH/2-140, self.PAGE_WIDTH-190, self.exam_dict['sample_type'])
		canvas.drawString(self.PAGE_WIDTH/2+20, self.PAGE_WIDTH-190,self.exam_dict['send_people'])
		canvas.drawString(self.PAGE_WIDTH/2+170, self.PAGE_WIDTH-190, self.exam_dict['check_date'])
		
		if not exam_dict.has_key(""):
			self.exam_dict['report_date']=datetime.datetime.now().strftime('%Y/%m/%d')  
		
		canvas.drawString(self.PAGE_WIDTH/2+310, self.PAGE_WIDTH-190, self.exam_dict['report_date'])
		#third Line title Name
		canvas.drawString(self.PAGE_WIDTH/2-140, self.PAGE_WIDTH-210,self.exam_dict['check_method'])
		canvas.drawString(self.PAGE_WIDTH/2+30, self.PAGE_WIDTH-210, self.exam_dict['unit'])
		#clinical log
		canvas.setFont('hei', 13)
		canvas.drawString(self.PAGE_WIDTH/2-195, self.PAGE_WIDTH-235, u"临床信息")
		canvas.setFont('song', 11)
	
	def insertClinicalAnnotation(self):
		flow_list=[]
		normalStyle=self.DefaultParagraphStyle
		if self.__ParaDelimiter in self.exam_dict['annotation']:  #------包含多个段落------#
			paras=self.exam_dict['annotation'].split(self.__ParaDelimiter)
			for para in paras:
				new_para=Paragraph(para.strip(),normalStyle)
				flow_list.append(new_para)
		else:     #---只包含一段---------------#
			para=Paragraph(self.exam_dict['annotation'], normalStyle)
			flow_list.append(para)
		return flow_list
		
	def myLaterPages(self,canvas, doc):  
		self.__insertTitle(canvas,doc)
		canvas.saveState()
		I=Image(self.__LogoPath)
		I.hAlign="LEFT"
		I.drawWidth=3*inch
		drawHeight = 3*inch*I.drawHeight / I.drawWidth-0.5*inch
		drawWidth = 3*inch
		canvas.drawInlineImage(self.__LogoPath,0.8*inch,6.7*inch,drawWidth,drawHeight)
		canvas.setFont(self.__PageNumFontName, self.__PageNumFontSize)
		canvas.drawString((self.PAGE_WIDTH/2)+150,50,u"%d" % (doc.page))
		canvas.restoreState()
	
	def insertPageLogo(self):
		I=Image(self.__LogoPath)
		I.hAlign="LEFT"
		I.drawHeight = 3*inch*I.drawHeight / I.drawWidth
		I.drawWidth = 3*inch
		return I
	
	#################添加检测人和审核人签名################################
	def insertSignature(self,flow_list):
		paraStyle=self.__setDefaultParagraphStyle(self.__Config)
		paraStyle.fontName="hei"
		paraStyle.fontSize=12
		paraStyle.leftIndent=3.6*inch
		flow_list.append(Spacer(4*inch,1*inch))
		para=Paragraph(u"检测人：",paraStyle)
		flow_list.append(para)
		exam=Image(self.__ExamineSignature)
		exam.hAlign="CENTER"
		exam.drawHeight = 1*inch*exam.drawHeight / exam.drawWidth
		exam.drawWidth = 1*inch
		flow_list.append(Spacer(4*inch,-0.5*inch))
		flow_list.append(exam)
		flow_list.append(Spacer(4*inch,-0.6*inch))
		 
		secondParaStyle=self.__setDefaultParagraphStyle(self.__Config)
		secondParaStyle.fontName="hei"
		secondParaStyle.fontSize=12
		secondParaStyle.leftIndent=7.9*inch
		seondPara=Paragraph(u"审核人：",secondParaStyle)
		flow_list.append(seondPara)
		chec=Image(self.__CheckSignature)
		chec.hAlign="RIGHT" 
		chec.drawHeight = 1*inch*chec.drawHeight / chec.drawWidth
		chec.drawWidth = 1*inch
		flow_list.append(Spacer(6*inch,-0.4*inch))
		flow_list.append(chec)
		return flow_list
	
	#################添加第二部分内容################################
	def  insertSecondPage(self):
		flow_list=[]
		paraStyle=self.__setDefaultParagraphStyle(self.__Config)
		paraStyle.fontName="hei"
		paraStyle.fontSize=13
		paraStyle.spaceBefore = 8
		paraStyle.spaceAfter =10
		para=Paragraph(u"核心报告内容",paraStyle)
		flow_list.append(para)
		
		#--------------------核心报告表1-----------------------------------------#
		coreTable1_data= [[u'突变基因', u'突变类型', u'突变位置', u'转录本\n编号', u'外显子\n编号', u'核苷酸\n变化', u'氨基酸\n变化', u'纯合/\n杂合', u'正常人\n频率', u'相关疾病', u'遗传模式',u'突变评定'],
		['NA', 'NA','NA','NA','NA','NA','NA','NA','NA','NA','NA','NA'],
		]
		coreTable1=Table(coreTable1_data,12*[0.8*inch],[0.4*inch,0.3*inch])
		coreTable1.setStyle(TableStyle([
		('TOPPADDING',(0,0),(-1,-1),10),
		('ALIGN',(0,0),(-1,-1),'CENTER'), 
		('BOX', (0,0), (-1,-1), 1, colors.black),
		('FONTNAME', (0,0), (-1,-1), 'hei'),
		('FONTSIZE', (0,0), (-1,-1), 11),
		('VALIGN', (0,1), (-1,1), 'MIDDLE'),
		('FONTNAME', (0,1), (-1,1), 'song'),
		('FONTSIZE', (0,1), (-1,1), 9),
		('INNERGRID', (0,0), (-1,-1), 0.5, colors.black)
		]))
		flow_list.append(coreTable1)
		#----------------------标注信息----------------------------#
		paraStyle.fontName="song"
		paraStyle.fontSize=9
		paraStyle.spaceBefore = 1
		paraStyle.spaceAfter =0
		paraStyle.leftIndent=3
		para=Paragraph(u"注：参考基因组版本号为 GRCh37/hg19；hom/het:hom 表示此突变位点为纯合突变，het 表示此突变位点为杂合突变；正常人频率为千人基因组中该突变频率。",paraStyle)
		flow_list.append(para)
		
		flow_list.append(Spacer(1, 0.2*inch))
		#-----------------------核心报告表2------------------------------#
		coreTable2_data=[[u'遗传模式',u'检测结果'],[u'Autosomal dominate',u'未见表型匹配致病位点，结果阴性'],[u'Autosomal recessive',u'未见表型匹配致病位点，结果阴性'],[u'Compound heterozygous',u'未见表型匹配致病位点，结果阴性'],[u'Xlinked inheritance',u'未见表型匹配致病位点，结果阴性']]
		coreTable2=Table(coreTable2_data,2*[2.9*inch],5*[0.4*inch],hAlign="LEFT")
		coreTable2.setStyle(TableStyle([
		('TOPPADDING',(0,0),(-1,-1),20),
		('ALIGN',(0,0),(-1,-1),'CENTER'),
		('BOX', (0,0), (-1,-1), 1, colors.black),
		('FONTNAME', (0,0), (-1,-1), 'hei'),
		('FONTSIZE', (0,0), (-1,-1), 11),
		('FONTNAME', (0,1), (-1,-1), 'song'),
		('FONTSIZE', (0,1), (-1,-1), 9),
		('INNERGRID', (0,0), (-1,-1), 0.5, colors.black)
		]))
		flow_list.append(coreTable2)
		#------------------------------医师签名-------------------------#
		flow_list=self.insertSignature(flow_list)
		return flow_list
	
	###################处理字典中包含多个段落的键值#######################
	def dealMultiParagraph(self,dict,dict_item):
		flow_list=[]
		normalStyle=self.DefaultParagraphStyle
		if self.__ParaDelimiter in dict[dict_item]:  #------包含多个段落------#
			paras=dict[dict_item].split(self.__ParaDelimiter)
			for para in paras:
				new_para=Paragraph(para.strip(),normalStyle)
				flow_list.append(new_para)
		else:     #---只包含一段---------------#
			para=Paragraph(dict[dict_item], normalStyle)
			flow_list.append(para)
		return flow_list
		
	######################################第三部分检测结论############################
	def insertThirdPage(self):
		flow_list=[]
		horizon_top=Image(self.__HorizonTopImagePath)
		horizon_top.hAlign="CENTER"
		horizon_top.drawHeight = 0.02*inch
		horizon_top.drawWidth=self.PAGE_WIDTH+1.8*inch
		flow_list.append(horizon_top)
		paraStyle=self.__setDefaultParagraphStyle(self.__Config)
		paraStyle.fontName="hei"
		paraStyle.fontSize=12
		paraStyle.spaceBefore = 8
		paraStyle.spaceAfter =10
		para=Paragraph(u"检测结论:",paraStyle)
		flow_list.append(para)
		normalStyle=self.__setDefaultParagraphStyle(self.__Config)
		paras=self.dealMultiParagraph(self.exam_dict,"check_conclusion")
		#para=Paragraph(u"本次 WES 检测未检出和患者表型一致的突变位点。针对患者表型进一步查阅相关资料发现，家族遗传性上睑下垂主要有三种形式：仅上睑下垂；上睑下垂并伴有眼肌瘫痪；上睑下垂并伴有睑裂狭小。已有文献报道有两个相关基因：PTOS1，PTOS2。其中 PTOS1（OMIM：178300）突变可引起常染色体显性遗传疾病“遗传性上睑下垂 1 型”，主要表型为上睑下垂。Engle et al. [2] 通过对一个患病家庭进行研究，使用 FISH 鉴定 YAC 文库将基因定位到了 1p34.1-p32 区间 （chr1:43,700,000-60,800,000 ）;McMullan et al. [3] 通过对一个遗传性双边孤立眼睑下垂 (congenital bilateral isolated ptosis) 男性患者进行研究， 将基因定位到离 1p34.1-p32 区间 13Mb 的位置，并在老鼠中找到同源基因 ZFHX4; Nakashima et al. [4] 通过连锁分析将基因定位到 8q21.1, 12q24.3, 及 14q22.3 三个位置。PTOS2 (OMIM:300245)突变可引起 X 连锁显性遗传疾病“遗传性上睑下垂 2 型”，主要表型为下巴抬高，上睑下垂，双边提肌，上睑无褶皱，前额突出 。McMullan et al. [2] 通过对一个家族性上睑下垂家庭研究，将基因定位到 X 染色体 Xq24-q27.1 区间。综上，目前关于眼睑下垂的研究还没有明确的相关致病基因位置，只是给出了大致基因区间。以上结果请结合家系和临床进一步分析。", normalStyle)
		flow_list.extend(paras)
		
		horizon_bottom=Image(self.__HorizonTopImagePath)
		horizon_bottom.hAlign="CENTER"
		horizon_bottom.drawHeight = 0.01*inch
		horizon_bottom.drawWidth=self.PAGE_WIDTH+1.8*inch
		flow_list.append(horizon_bottom)
		return flow_list
	##########################添加第四部分参考文献信息##################################
	def  insertForthPage(self):
		flow_list=[]
		paraStyle=self.__setDefaultParagraphStyle(self.__Config)
		paraStyle.fontName="hei"
		paraStyle.fontSize=12
		paraStyle.spaceBefore = 5
		paraStyle.spaceAfter =2
		para=Paragraph(u"参考文献",paraStyle)
		flow_list.append(para)
		
		horizon_top=Image(self.__HorizonBottomImagePath)
		horizon_top.hAlign="CENTER"
		horizon_top.drawHeight = 0.035*inch
		horizon_top.drawWidth=self.PAGE_WIDTH+1.8*inch
		flow_list.append(horizon_top)
		
		normalStyle=self.__setDefaultParagraphStyle(self.__Config)
		normalStyle.fontSize=9
		normalStyle.leading=12
		paras=self.dealMultiParagraph(self.exam_dict,"articles")
		flow_list.extend(paras)
		
		horizon_top=Image(self.__HorizonBottomImagePath)
		horizon_top.hAlign="CENTER"
		horizon_top.drawHeight = 0.035*inch
		horizon_top.drawWidth=self.PAGE_WIDTH+1.8*inch
		flow_list.append(horizon_top)
		
		paraStyle=self.__setDefaultParagraphStyle(self.__Config)
		paraStyle.fontName="hei"
		paraStyle.fontSize=11
		paraStyle.spaceBefore = 5
		paraStyle.spaceAfter =2
		paraStyle.leading=15  
		para=Paragraph(u"备注：",paraStyle)
		flow_list.append(para)
		
		paraStyle=self.__setDefaultParagraphStyle(self.__Config)
		paraStyle.fontSize=8
		paraStyle.leading=12
		paras=self.dealMultiParagraph(self.exam_dict,"remarks")
		flow_list.extend(paras)
	
		return flow_list
	##########################添加第五部分 扩展报告##################################
	def insertFifthPage(self):
		flow_list=[]
		paraStyle=self.__setDefaultParagraphStyle(self.__Config)
		paraStyle.fontName="hei"
		paraStyle.fontSize=12
		paraStyle.spaceBefore = 5
		paraStyle.spaceAfter =2
		para=Paragraph(u"扩展报告内容：",paraStyle)
		flow_list.append(para)
		
		normalStyle=self.__setDefaultParagraphStyle(self.__Config)
		normalStyle.fontSize=10
		normalStyle.fontName="song"
		normalStyle.leading = 6
		para=Paragraph(u'Familial thoracic  aortic aneurysm and section',normalStyle)
		#----------------扩展表数据-------------------------#
		extend_table_data=[[u'突变基因', u'突变类型', u'突变位置', u'转录本\n编号', u'外显子\n编号', u'核苷酸\n变化', u'氨基酸\n变化', u'纯合/\n杂合', u'正常人\n频率', u'相关疾病', u'遗传模式',u'突变评定'],
		[u'MYLK',u'splicing',u'chr3:123368043\n-123368043',u'NM_053028',u'exon24',u'c.4082-2->C',u'.',u'het',u'0.0089',para,u'AD',u'Likely \n pathogenic'],
		[u'MYLK',u'splicing',u'chr3:123368043\n-123368043',u'NM_053028',u'exon24',u'c.4082-2->C',u'.',u'het',u'0.0089',u'Familial thoracic \n aortic aneurysm and  \n aortic dissection',u'AD',u'Likely \n pathogenic'],
		[u'MYLK',u'splicing',u'chr3:123368043\n-123368043',u'NM_053028',u'exon24',u'c.4082-2->C',u'.',u'het',u'0.0089',u'Familial thoracic \n aortic aneurysm and  \n aortic dissection',u'AD',u'Likely \n pathogenic'],
		[u'MYLK',u'splicing',u'chr3:123368043\n-123368043',u'NM_053028',u'exon24',u'c.4082-2->C',u'.',u'het',u'0.0089',u'Familial thoracic \n aortic aneurysm and  \n aortic dissection',u'AD',u'Likely \n pathogenic'],
		[u'MYLK',u'splicing',u'chr3:123368043\n-123368043',u'NM_053028',u'exon24',u'c.4082-2->C',u'.',u'het',u'0.0089',u'Familial thoracic \n aortic aneurysm and  \n aortic dissection',u'AD',u'Likely \n pathogenic'],
		[u'MYLK',u'splicing',u'chr3:123368043\n-123368043',u'NM_053028',u'exon24',u'c.4082-2->C',u'.',u'het',u'0.0089',u'Familial thoracic \n aortic aneurysm and  \n aortic dissection',u'AD',u'Likely \n pathogenic'],
		[u'MYLK',u'splicing',u'chr3:123368043\n-123368043',u'NM_053028',u'exon24',u'c.4082-2->C',u'.',u'het',u'0.0089',u'Familial thoracic \n aortic aneurysm and  \n aortic dissection',u'AD',u'Likely \n pathogenic'],
		[u'MYLK',u'splicing',u'chr3:123368043\n-123368043',u'NM_053028',u'exon24',u'c.4082-2->C',u'.',u'het',u'0.0089',u'Familial thoracic \n aortic aneurysm and  \n aortic dissection',u'AD',u'Likely \n pathogenic'],
		[u'MYLK',u'splicing',u'chr3:123368043\n-123368043',u'NM_053028',u'exon24',u'c.4082-2->C',u'.',u'het',u'0.0089',u'Familial thoracic \n aortic aneurysm and  \n aortic dissection',u'AD',u'Likely \n pathogenic'],
		[u'MYLK',u'splicing',u'chr3:123368043\n-123368043',u'NM_053028',u'exon24',u'c.4082-2->C',u'.',u'het',u'0.0089',u'Familial thoracic \n aortic aneurysm and  \n aortic dissection',u'AD',u'Likely \n pathogenic'],
			];
		extend_table=Table(extend_table_data,[0.7*inch,0.8*inch,1.0*inch,0.9*inch,0.65*inch,0.8*inch,0.7*inch,0.55*inch,0.7*inch,1.2*inch,0.8*inch,0.8*inch],11*[0.7*inch])
		extend_table.setStyle(TableStyle([
		('TOPPADDING',(0,0),(-1,-1),5),
		('LEFTPADDING',(0,0),(-1,-1),10),
		('LEADING',(0,0),(-1,-1),10),
		('ALIGN',(0,0),(-1,-1),'CENTER'),
		('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
		('BOX', (0,0), (-1,-1), 1, colors.black),
		('FONTNAME', (0,0), (-1,-1), 'hei'),
		('FONTSIZE', (0,0), (-1,-1), 10),
		('VALIGN', (0,1), (-1,1), 'MIDDLE'),
		('FONTNAME', (0,1), (-1,-1), 'song'),
		('FONTSIZE', (0,1), (-1,-1), 9),
		('INNERGRID', (0,0), (-1,-1), 0.5, colors.black)
		]))
		flow_list.append(extend_table)
		paraStyle=self.__setDefaultParagraphStyle(self.__Config)
		paraStyle.fontName="song"
		paraStyle.fontSize=7
		paraStyle.spaceBefore =2
		paraStyle.spaceAfter =0
		paraStyle.leading=10
		para=Paragraph(u"注：该扩展报告内容为与检测过程中筛选的与临床表型不符的致病性或疑似致病性突变位点，经遗传模式、发病年龄、人群频率过滤，选择可能具有临床监控意义的位点报出，结果仅供临床参考。其中遗传模式缩写解释：AD 指常染色体显性遗传；AR 指常染色体隐性遗传；Mu:指多因子遗传。",paraStyle)
		flow_list.append(para)
		
		return flow_list  
	#############################第六部分 插入数据质控信息#############################
	def insertSixthPage(self):
		flow_list=[]
		paraStyle=self.__setDefaultParagraphStyle(self.__Config)
		paraStyle.fontName="hei"
		paraStyle.fontSize=13
		para=Paragraph(u'附件一.数据质控信息',paraStyle)
		flow_list.append(para)
		qc_table_data=[[u'样本名称',self.exam_dict['code']],[u'目标区域捕获效率',self.exam_dict['target_efficiency']],[u'目标区域覆盖度',self.exam_dict['target_cover']],[u'覆盖 4X 以上区域占比',self.exam_dict['cover_4x']],[u'覆盖 20X 以上区域占比',self.exam_dict['cover_20x']],[u'平均测序深度',self.exam_dict['average_deep']]]
		qc_table=Table(qc_table_data,2*[3*inch],6*[0.3*inch],hAlign="LEFT")
		qc_table.setStyle(TableStyle([
		('TOPPADDING',(0,0),(-1,-1),5),
		('LEFTPADDING',(0,0),(-1,-1),10),
		('LEADING',(0,0),(-1,-1),10),
		('ALIGN',(0,0),(-1,-1),'LEFT'),
		('BOX', (0,0), (-1,-1), 1, colors.black),
		('FONTNAME', (0,0), (-1,-1), 'hei'),
		('FONTSIZE', (0,0), (-1,-1), 10),
		('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
		('INNERGRID', (0,0), (-1,-1), 0.5, colors.black)
		]))
		flow_list.append(qc_table)
		return flow_list
		
	def renderPDF(self,report_name):
		Story=[]
		#reverse the default A4 page and rotate the width and height
		Horiz_A4=(29.7*cm,21*cm)
		report_path=os.path.join(self.report_output_path,report_name)
		doc = SimpleDocTemplate(report_path,pagesize=Horiz_A4) 
		doc.topMargin=1.5*inch
		#################First Part#########################################################
		#--------------insert clinical information---------------------#
		Story.append(Spacer(1, 1.9*inch))  
		Story.extend(self.insertClinicalAnnotation())
		Story.append(PageBreak())
		#################Second  Part########################################################		  
		Story.extend(self.insertSecondPage())
		Story.append(PageBreak())
		#####################Third Part#################################################	  
		Story.extend(self.insertThirdPage())
		Story.append(PageBreak())
		#####################Fourth  Part###############################################
		Story.extend(self.insertForthPage())
		Story.append(PageBreak())
		#####################Fifth Part################################################	 
		Story.extend(self.insertFifthPage())
		Story.append(PageBreak())
		####################Sixth Part################################################
		Story.extend(self.insertSixthPage())
		Story.append(PageBreak())
		  
		doc.build(Story,onFirstPage=self.myFirstPage,onLaterPages=self.myLaterPages)
		
if   __name__=="__main__":
	exam_dict={'name':u'王昆','code':u'6E013','sex':u'男','age':u'45','sample_type':u'外周血','send_people':u'何蓉','check_date':u'2016/09/26','check_method':u'WES检测','unit':u'中国医科大学附属盛京医院','annotation':u'临床印象与送检疾病：家族遗传病：父亲、姑姑、爷爷均有症状；诊断结果：眼睑下垂；其他临床信息说明：出生后出现单眼上眼睑重度下垂，染色体正常。<para>受检者个人史及体查：眼：眼睑下垂。以下均为正常：头部、眼区、耳、鼻、上颌与下颌、口、牙齿、颈部、胸部、腹部、上肢、下肢、关节、皮肤与毛发、泌尿生殖系统、哭声、心脏、肾脏、神经系统、内分泌系统和代谢；以下均为无：免疫缺陷、血液疾病及肿瘤、罕见的生长形态、其他特殊异常表征、不良孕产史。<para>其他检查报告结果：检测产品：SWES-01_JZ4000；检测方法：安捷伦外显子芯片捕获+高通量测序；检测结果：从受检者外周血中提取基因组 DNA，经由构建基因组 DNA 文库、富集目标 DNA 片段、高通量测序（Illumina，美国）、生物信息专业软件分析测序数据。该样本在所检测范围内未见明确致病改变。在先天性肌无力综合征 2C 型，乙酰胆碱受体缺乏相关、先天性肌无力综合征 2A 型，慢通道相关基因CHRNB1存在一处杂合突变，家系验证结果显示此突变来自于其母，请结合表型症状进一步分析。王昆之姑家系验证报告结果解读：王昆之姑 CHRNB1 基因 c.107C>G 位点无突变，请结合临床进一步分析。',
	'check_conclusion':u"本次 WES 检测未检出和患者表型一致的突变位点。<para>针对患者表型进一步查阅相关资料发现，家族遗传性上睑下垂主要有三种形式：仅上睑下垂；上睑下垂并伴有眼肌瘫痪；上睑下垂并伴有睑裂狭小。已有文献报道有两个相关基因：PTOS1，PTOS2。其中 PTOS1（OMIM：178300）突变可引起常染色体显性遗传疾病“遗传性上睑下垂 1 型”，主要表型为上睑下垂。Engle et al. [2] 通过对一个患病家庭进行研究，使用 FISH 鉴定 YAC 文库将基因定位到了 1p34.1-p32 区间 （chr1:43,700,000-60,800,000 ）;McMullan et al. [3] 通过对一个遗传性双边孤立眼睑下垂 (congenital bilateral isolated ptosis) 男性患者进行研究， 将基因定位到离 1p34.1-p32 区间 13Mb 的位置，并在老鼠中找到同源基因 ZFHX4; Nakashima et al. [4] 通过连锁分析将基因定位到 8q21.1, 12q24.3, 及 14q22.3 三个位置。PTOS2 (OMIM:300245)突变可引起 X 连锁显性遗传疾病“遗传性上睑下垂 2 型”，主要表型为下巴抬高，上睑下垂，双边提肌，上睑无褶皱，前额突出 。McMullan et al. [2] 通过对一个家族性上睑下垂家庭研究，将基因定位到 X 染色体 Xq24-q27.1 区间。综上，目前关于眼睑下垂的研究还没有明确的相关致病基因位置，只是给出了大致基因区间。<para>以上结果请结合家系和临床进一步分析。",
	'articles':u"[1] Richards S, Aziz N, Bale S, et al. Standards and guidelines for the interpretation of sequence variants: a joint consensus recommendation of the American College of Medical Genetics and Genomics and the Association for Molecular Pathology. Genetics in Medicine, 2015; 17(5):405-424.<para>[2] Engle E C, Castro A E, Macy M E, et al. A gene for isolated congenital ptosis maps to a 3-cM region within 1p32-p34.1.[J]. American Journal of Human Genetics, 1997, 60(5):1150-7.<para>[3] Mcmullan T F W, Collins A R, Tyers A G, et al. A Novel X-Linked Dominant Condition: X-Linked Congenital Isolated Ptosis[J]. American Journal of Human Genetics, 2000, 66(4):1455-60.<para>[4] Nakashima M, Nakano M, Hirano A, et al. Genome-wide linkage analysis and mutation analysis of hereditary congenital blepharoptosis in a Japanese family[J]. Journal of Human Genetics, 2008, 53(1):34-41.",
	'remarks':u"1.&nbsp; &nbsp;&nbsp;本报告结果只对本次送检样品负责。<para>2.&nbsp; &nbsp;&nbsp;以上结论均为实验室检测数据，仅用于突变检测之目的，不代表最终诊断结果，仅供临床参考。<para>3.&nbsp; &nbsp;&nbsp;数据解读规则参考美国医学遗传学和基因组学学院相关指南。<para>4.&nbsp; &nbsp;&nbsp;变异命名参照 HGVS 建议的规则给出(<font color='blue'>http://www.hgvs.org/mutnomen/</font>)<para>5.&nbsp; &nbsp;&nbsp;本检测只针对基因外显子部分，报告的突变类型包括：突变包括移码突变(frameshift insertion/deletion)、整码突变(inframe insertion/deletion)、非同义突变(nonsynonymous variant )、剪切区域突变(splice region/donor/acceptor variant)；对于同义突变(synonymous variant)、非编码区突变(UTR variant)、内含子突变(intron variant)不做报告。<para>6.&nbsp; &nbsp;&nbsp;本结果已经过滤掉了千人基因组，ExAC03，ESP6500 等数据库中突变频率大于 5%的突变位点。<para>7.&nbsp; &nbsp;&nbsp;本结果所用数据库版本：Human Genome hg19/GRCh37、RefSeq (release 61)、dbSNP (v144)、1000 Genomes phase3、esp6500、ExAC03。<para>8.&nbsp; &nbsp;&nbsp;参考基因组是人类 hg19 版本。<para>9.&nbsp; &nbsp;&nbsp;核心报告内容为本次检测得到的与所提供临床表型相关的致病或疑似致病位点，并进行了一代测序验证。<para>10.&nbsp; &nbsp;&nbsp;扩展报告内容为本次检测得到的与所提供临床表型不符，但判读为致病或疑似致病的位点，未进行一代测序验证。",
	'target_efficiency':'66.08%','target_cover':'97.25%','cover_4x':'96.79%','cover_20x':'95.22%','average_deep':"113.10"
	}
	s=wesReport("./",exam_dict)
	s.renderPDF("test.pdf")