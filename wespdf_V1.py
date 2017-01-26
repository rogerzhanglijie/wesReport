#coding=utf-8
#Author:Roger Zhang
#Date:2017-01-22
#Edition:First
#Function: This script is used to convert the log parameters to pdf document format


#设定初始化参数
#params: defaultFontSize 默认字体大小 20
def init_config(defaultFontSize=20):
	import reportlab.rl_config
	reportlab.rl_config.warnOnMissingFontGlyphs = 0
	from reportlab.pdfbase import pdfmetrics
	from reportlab.pdfbase.ttfonts import TTFont
	import copy
	pdfmetrics.registerFont(TTFont('song', 'font/SURSONG.TTF'))
	pdfmetrics.registerFont(TTFont('hei', 'font/SIMHEI.TTF'))
	stylesheet= getSampleStyleSheet()
	styles= copy.deepcopy(stylesheet['Normal'])
	styles.fontName ='song'
	styles.fontSize = defaultFontSize
	return styles
from reportlab.platypus import *
from reportlab.lib.styles import getSampleStyleSheet   
from reportlab.rl_config import defaultPageSize   
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import *
#from reportlab.lib.utils import *
from reportlab.lib.units import mm
from reportlab.lib import colors  
styles=init_config() 
PAGE_HEIGHT=defaultPageSize[1]   
PAGE_WIDTH=defaultPageSize[0]
Title = u"科技关爱生命"  
ReportName=u"全外显子组测序检验报告"
pageinfo = "platypus example"  
Story=[]

#############首页模板样式#############################################
def myFirstPage(canvas,doc):  
	#insert Image Logo on the header
	insertTitle(canvas,doc)
	canvas.saveState()   
	canvas.setFont('hei', 16)
	#insert top-bottom line
	insertTwoHorizonLines(canvas,doc)
	#insert Report Name
	canvas.drawCentredString(PAGE_HEIGHT/2-100, PAGE_HEIGHT-150, ReportName)
	#insert Clinical Test Data
	insertClinicalTest(canvas,doc)
	canvas.setFont('song', 9)
	canvas.drawString((PAGE_WIDTH/2)-20,10,u"1")   
	canvas.restoreState()
#######################################################################################################

	
#insert clinical test information, which contain name,code,sex and so on
def insertClinicalTest(canvas,doc):
	canvas.setFont('hei', 10)
	canvas.drawString(PAGE_HEIGHT/2-350, PAGE_HEIGHT-180, u"受检者信息")
	canvas.setFont('hei', 9)
	#first Line title
	canvas.drawString(PAGE_HEIGHT/2-350, PAGE_HEIGHT-200, u"受检者姓名：")
	canvas.drawString(PAGE_HEIGHT/2-240, PAGE_HEIGHT-200, u"样本标号：")
	canvas.drawString(PAGE_HEIGHT/2-130, PAGE_HEIGHT-200, u"性别：")
	canvas.drawString(PAGE_HEIGHT/2-10, PAGE_HEIGHT-200, u"年龄：")
	#second Line title
	canvas.drawString(PAGE_HEIGHT/2-350, PAGE_HEIGHT-220, u"样本类型：")
	canvas.drawString(PAGE_HEIGHT/2-240, PAGE_HEIGHT-220, u"送捡人：")
	canvas.drawString(PAGE_HEIGHT/2-130, PAGE_HEIGHT-220, u"送检日期：")
	canvas.drawString(PAGE_HEIGHT/2-10, PAGE_HEIGHT-220, u"报告日期：")
	#third Line title
	canvas.drawString(PAGE_HEIGHT/2-350, PAGE_HEIGHT-240, u"检测方法：")
	canvas.drawString(PAGE_HEIGHT/2-240, PAGE_HEIGHT-240, u"送捡单位：")
	
	canvas.setFont('song', 9)
	#first Line title Name
	canvas.drawString(PAGE_HEIGHT/2-290, PAGE_HEIGHT-200, u"王坤")
	canvas.drawString(PAGE_HEIGHT/2-190, PAGE_HEIGHT-200, u"DE321")
	canvas.drawString(PAGE_HEIGHT/2-100, PAGE_HEIGHT-200, u"男")
	canvas.drawString(PAGE_HEIGHT/2+20, PAGE_HEIGHT-200, u"35")
	#second Line title Name
	canvas.drawString(PAGE_HEIGHT/2-300, PAGE_HEIGHT-220, u"外周血")
	canvas.drawString(PAGE_HEIGHT/2-200, PAGE_HEIGHT-220, u"何蓉")
	canvas.drawString(PAGE_HEIGHT/2-80, PAGE_HEIGHT-220, u"2016/8/26")
	canvas.drawString(PAGE_HEIGHT/2+40, PAGE_HEIGHT-220, u"2017/1/23")
	#third Line title Name
	canvas.drawString(PAGE_HEIGHT/2-300, PAGE_HEIGHT-240, u"WES检测")
	canvas.drawString(PAGE_HEIGHT/2-190, PAGE_HEIGHT-240, u"中国医科大学附属盛京医院")
	#clinical log
	canvas.setFont('hei', 10)
	canvas.drawString(PAGE_HEIGHT/2-350, PAGE_HEIGHT-280, u"临床信息")
	canvas.setFont('song', 9)
	
def insertTwoHorizonLines(canvas,doc):
	# 设置线的颜色
	canvas.setStrokeColorRGB(0,0,0)
	# 绘制线
	#insert top line
	canvas.line(0.8*inch,9.5*inch,7.8*inch,9.5*inch) 
	#insert middle line
	canvas.line(0.8*inch,8.1*inch,7.8*inch,8.1*inch) 
	#insert Bottom Line
	canvas.line(0.8*inch,0.8*inch,7.8*inch,0.8*inch) 

#添加临床医生诊断信息
def insertClinicalAnnotation():
	normalStyle=setDefaultParagrahStyle()
	para=Paragraph(u"<para>临床印象与送检疾病：家族遗传病：父亲、姑姑、爷爷均有症状；诊断结果：眼睑下垂；其他临床信息说明：出生后出现单眼上眼睑重度下垂，染色体正常。<br/>受检者个人史及体查：眼：眼睑下垂。以下均为正常：头部、眼区、耳、鼻、上颌与下颌、口、牙齿、颈部、腹部、上肢、下肢、关节、皮肤与\n毛发、泌尿生殖系统、哭声、心脏、肾脏、神经系统、内分泌系统和代谢；以下均为无：免疫缺陷、血液疾病及肿瘤、罕见的生长形态、其他特殊异常表征、不良孕产史。<br/>其他检查报告结果：检测产品：SWES-01_JZ4000；检测方法：安捷伦外显子芯片捕获+高通量测序；检测结果：从受检者外周血中提取基因组 DNA，经由构建基因组 DNA 文库、富集目标 DNA 片段、高通量测序（Illumina，美国）、生物信息专业软件分析测序数据。该样本在所检测范围内未见明确致病改变。在先天性肌无力综合征 2C 型，乙酰胆碱受体缺乏相关、先天性肌无力综合征 2A 型，慢通道相关基因 CHRNB1 存在一处杂合突变，家系验证结果显示此突变来自于其母，请结合表型症状进一步分析。王昆之姑家系验证报告结果解读：王昆之姑 CHRNB1 基因 c.107C>G 位点无突变，请结合临床进一步分析。<br/></para>", normalStyle)
	return para  

#########设置默认段落样式#######################
def  setDefaultParagrahStyle():
	import copy
	stylesheet=getSampleStyleSheet()
	normalStyle = copy.deepcopy(stylesheet['Normal'])
	normalStyle.fontName ="song"
	normalStyle.leftIndent=0
	normalStyle.splitLongWords = 1
	normalStyle.spaceBefore = 2
	normalStyle.borderWidth=5
	normalStyle.borderPadding=5
	normalStyle.fontSize = 9
	normalStyle.leading = 20  #设置行间距
	return normalStyle
	
##################其他页面模板样式#############################################################		
def myLaterPages(canvas, doc):  
	insertTitle(canvas,doc)
	canvas.saveState()
	canvas.setFont('song', 9)
	canvas.drawString((PAGE_WIDTH/2)-20,10,u"%d" % (doc.page))
	canvas.restoreState()

	
#添加页面logo
#params: logoPath 存放页面logo的路径，默认存放在images/logo.jpg文件;
def insertPageLogo(logoPath="images/logo.jpg"):
	I=Image(logoPath)
	I.hAlign="LEFT"
	I.drawHeight = 2*inch*I.drawHeight / I.drawWidth
	I.drawWidth = 2*inch
	return I

###############添加检测者及医生签字########################################
def insertSignature(flow_list,signaturePath={"examine":"images/sign_zhang.jpg","check":"images/sign_yu.jpg"}):
	paraStyle=setDefaultParagrahStyle()
	paraStyle.fontName="hei"
	paraStyle.fontSize=10
	paraStyle.leftIndent=2*inch
	flow_list.append(Spacer(1,1*inch))
	para=Paragraph(u"检测人：",paraStyle)
	flow_list.append(para)
	exam=Image(signaturePath['examine'])
	exam.hAlign="CENTER"
	exam.drawHeight = 0.6*inch*exam.drawHeight / exam.drawWidth
	exam.drawWidth = 0.6*inch
	flow_list.append(Spacer(1,-0.4*inch))
	flow_list.append(exam)
	flow_list.append(Spacer(1,-0.4*inch))
	 
	secondParaStyle=setDefaultParagrahStyle()
	secondParaStyle.fontName="hei"
	secondParaStyle.fontSize=10
	secondParaStyle.leftIndent=4.9*inch
	seondPara=Paragraph(u"审核人：",secondParaStyle)
	flow_list.append(seondPara)
	chec=Image(signaturePath['check'])
	chec.hAlign="RIGHT"
	chec.drawHeight = 0.6*inch*chec.drawHeight / chec.drawWidth
	chec.drawWidth = 0.6*inch
	flow_list.append(Spacer(1,-0.32*inch))
	flow_list.append(chec)
	return flow_list
	
#添加公司title
def insertTitle(canvas,doc):
	canvas.saveState()
	canvas.setFont('song',10)
	canvas.drawCentredString((PAGE_HEIGHT/2)+80, PAGE_HEIGHT-108, Title)
	canvas.restoreState() 
	
def  insertSecondPage():
	flow_list=[]
	paraStyle=setDefaultParagrahStyle()
	paraStyle.fontName="hei"
	paraStyle.fontSize=12
	paraStyle.spaceBefore = 8
	paraStyle.spaceAfter =10
	para=Paragraph(u"核心报告内容",paraStyle)
	flow_list.append(para)
	
	#--------------------核心报告表1-----------------------------------------#
	coreTable1_data= [[u'突变基因', u'突变类型', u'突变位置', u'转录本\n编号', u'外显子\n编号', u'核苷酸\n变化', u'氨基酸\n变化', u'纯合/\n杂合', u'正常人\n频率', u'相关疾病', u'遗传模式',u'突变评定'],
	['NA', 'NA','NA','NA','NA','NA','NA','NA','NA','NA','NA','NA'],
	]
	coreTable1=Table(coreTable1_data,12*[0.53*inch],[0.45*inch,0.2*inch])
	coreTable1.setStyle(TableStyle([
	('TOPPADDING',(0,0),(-1,-1),10),
	('ALIGN',(0,0),(-1,-1),'CENTER'),
	('BOX', (0,0), (-1,-1), 1, colors.black),
	('FONTNAME', (0,0), (-1,-1), 'hei'),
    ('FONTSIZE', (0,0), (-1,-1), 8),
	('VALIGN', (0,1), (-1,1), 'MIDDLE'),
	('FONTNAME', (0,1), (-1,1), 'song'),
    ('FONTSIZE', (0,1), (-1,1), 6),
	('INNERGRID', (0,0), (-1,-1), 0.5, colors.black)
	]))
	flow_list.append(coreTable1)
	#----------------------标注信息----------------------------#
	paraStyle.fontName="song"
	paraStyle.fontSize=6
	paraStyle.spaceBefore = 1
	paraStyle.spaceAfter =0
	para=Paragraph(u"注：参考基因组版本号为 GRCh37/hg19；hom/het:hom 表示此突变位点为纯合突变，het 表示此突变位点为杂合突变；正常人频率为千人基因组中该突变频率。",paraStyle)
	flow_list.append(para)
	
	flow_list.append(Spacer(1, 0.2*inch))
	#-----------------------核心报告表2------------------------------#
	coreTable2_data=[[u'遗传模式',u'检测结果'],[u'Autosomal dominate',u'未见表型匹配致病位点，结果阴性'],[u'Autosomal recessive',u'未见表型匹配致病位点，结果阴性'],[u'Compound heterozygous',u'未见表型匹配致病位点，结果阴性'],[u'Xlinked inheritance',u'未见表型匹配致病位点，结果阴性']]
	coreTable2=Table(coreTable2_data,2*[2*inch],5*[0.25*inch],hAlign="LEFT")
	coreTable2.setStyle(TableStyle([
	('TOPPADDING',(0,0),(-1,-1),20),
	('ALIGN',(0,0),(-1,-1),'CENTER'),
	('BOX', (0,0), (-1,-1), 1, colors.black),
	('FONTNAME', (0,0), (-1,-1), 'hei'),
    ('FONTSIZE', (0,0), (-1,-1), 8),
	('FONTNAME', (0,1), (-1,-1), 'song'),
    ('FONTSIZE', (0,1), (-1,-1), 6),
	('INNERGRID', (0,0), (-1,-1), 0.5, colors.black)
	]))
	flow_list.append(coreTable2)
	#------------------------------医师签名-------------------------#
	flow_list=insertSignature(flow_list)
	
	return flow_list
	
######################################第三页检测结论############################
def insertThirdPage(horizonTopImagePath="images/horizon_top.jpg",horizonBottomPath="images/horizon_top.jpg"):
	flow_list=[]
	horizon_top=Image(horizonTopImagePath)
	horizon_top.hAlign="CENTER"
	horizon_top.drawHeight = 0.02*inch
	horizon_top.drawWidth=PAGE_WIDTH-1*inch
	flow_list.append(horizon_top)
	
	paraStyle=setDefaultParagrahStyle()
	paraStyle.fontName="hei"
	paraStyle.fontSize=12
	paraStyle.spaceBefore = 8
	paraStyle.spaceAfter =10
	para=Paragraph(u"检测结论:",paraStyle)
	flow_list.append(para)
	normalStyle=setDefaultParagrahStyle()
	para=Paragraph(u"本次 WES 检测未检出和患者表型一致的突变位点。针对患者表型进一步查阅相关资料发现，家族遗传性上睑下垂主要有三种形式：仅上睑下垂；上睑下垂并伴有眼肌瘫痪；上睑下垂并伴有睑裂狭小。已有文献报道有两个相关基因：PTOS1，PTOS2。其中 PTOS1（OMIM：178300）突变可引起常染色体显性遗传疾病“遗传性上睑下垂 1 型”，主要表型为上睑下垂。Engle et al. [2] 通过对一个患病家庭进行研究，使用 FISH 鉴定 YAC 文库将基因定位到了 1p34.1-p32 区间 （chr1:43,700,000-60,800,000 ）;McMullan et al. [3] 通过对一个遗传性双边孤立眼睑下垂 (congenital bilateral isolated ptosis) 男性患者进行研究， 将基因定位到离 1p34.1-p32 区间 13Mb 的位置，并在老鼠中找到同源基因 ZFHX4; Nakashima et al. [4] 通过连锁分析将基因定位到 8q21.1, 12q24.3, 及 14q22.3 三个位置。PTOS2 (OMIM:300245)突变可引起 X 连锁显性遗传疾病“遗传性上睑下垂 2 型”，主要表型为下巴抬高，上睑下垂，双边提肌，上睑无褶皱，前额突出 。McMullan et al. [2] 通过对一个家族性上睑下垂家庭研究，将基因定位到 X 染色体 Xq24-q27.1 区间。综上，目前关于眼睑下垂的研究还没有明确的相关致病基因位置，只是给出了大致基因区间。以上结果请结合家系和临床进一步分析。", normalStyle)
	flow_list.append(para)
	
	horizon_bottom=Image(horizonBottomPath)
	horizon_bottom.hAlign="CENTER"
	horizon_bottom.drawHeight = 0.01*inch
	horizon_bottom.drawWidth=PAGE_WIDTH-1*inch
	flow_list.append(horizon_bottom)
	return flow_list

	
def  insertForthPage(horizonTopImagePath="images/horizon_bottom.jpg"):
	flow_list=[]
	paraStyle=setDefaultParagrahStyle()
	paraStyle.fontName="hei"
	paraStyle.fontSize=12
	paraStyle.spaceBefore = 5
	paraStyle.spaceAfter =2
	para=Paragraph(u"参考文献",paraStyle)
	flow_list.append(para)
	
	horizon_top=Image(horizonTopImagePath)
	horizon_top.hAlign="CENTER"
	horizon_top.drawHeight = 0.035*inch
	horizon_top.drawWidth=PAGE_WIDTH-2*inch
	flow_list.append(horizon_top)
	
	normalStyle=setDefaultParagrahStyle()
	normalStyle.fontSize=7
	para=Paragraph(u"[1] Richards S, Aziz N, Bale S, et al. Standards and guidelines for the interpretation of sequence variants: a joint consensus recommendation of the American College of Medical Genetics and Genomics and the Association for Molecular Pathology. Genetics in Medicine, 2015; 17(5):405-424.",normalStyle)
	flow_list.append(para)
	normalStyle=setDefaultParagrahStyle()
	normalStyle.fontSize=7
	para=Paragraph(u"[2] Engle E C, Castro A E, Macy M E, et al. A gene for isolated congenital ptosis maps to a 3-cM region within 1p32-p34.1.[J]. American Journal of Human Genetics, 1997, 60(5):1150-7.",normalStyle)
	flow_list.append(para)
	normalStyle=setDefaultParagrahStyle()
	normalStyle.fontSize=7
	para=Paragraph(u"[3] Mcmullan T F W, Collins A R, Tyers A G, et al. A Novel X-Linked Dominant Condition: X-Linked Congenital Isolated Ptosis[J]. American Journal of Human Genetics, 2000, 66(4):1455-60.",normalStyle)
	flow_list.append(para)
	normalStyle=setDefaultParagrahStyle()
	normalStyle.fontSize=7
	para=Paragraph(u"[4] Nakashima M, Nakano M, Hirano A, et al. Genome-wide linkage analysis and mutation analysis of hereditary congenital blepharoptosis in a Japanese family[J]. Journal of Human Genetics, 2008, 53(1):34-41.",normalStyle)
	flow_list.append(para)
	
	horizon_top=Image(horizonTopImagePath)
	horizon_top.hAlign="CENTER"
	horizon_top.drawHeight = 0.035*inch
	horizon_top.drawWidth=PAGE_WIDTH-2*inch
	flow_list.append(horizon_top)
	
	paraStyle=setDefaultParagrahStyle()
	paraStyle.fontName="hei"
	paraStyle.fontSize=8
	paraStyle.spaceBefore = 5
	paraStyle.spaceAfter =2
	para=Paragraph(u"备注：",paraStyle)
	flow_list.append(para)
	
	paraStyle=setDefaultParagrahStyle()
	paraStyle.fontName="song"
	paraStyle.fontSize=7
	paraStyle.spaceBefore = 0
	paraStyle.spaceAfter =0
	paraStyle.leading=10
	para=Paragraph(u"1.&nbsp; &nbsp;&nbsp;本报告结果只对本次送检样品负责。",paraStyle)
	flow_list.append(para)
	
	para=Paragraph(u"2.&nbsp; &nbsp;&nbsp;以上结论均为实验室检测数据，仅用于突变检测之目的，不代表最终诊断结果，仅供临床参考。",paraStyle)
	flow_list.append(para)
	
	para=Paragraph(u"3.&nbsp; &nbsp;&nbsp;数据解读规则参考美国医学遗传学和基因组学学院相关指南。",paraStyle)
	flow_list.append(para)
	
	para=Paragraph(u"4.&nbsp; &nbsp;&nbsp;变异命名参照 HGVS 建议的规则给出(<font color='blue'>http://www.hgvs.org/mutnomen/</font>)",paraStyle)
	flow_list.append(para)
	
	para=Paragraph(u"5.&nbsp; &nbsp;&nbsp;本检测只针对基因外显子部分，报告的突变类型包括：突变包括移码突变(frameshift insertion/deletion)、整码突变(inframe insertion/deletion)、非同义突变(nonsynonymous variant )、剪切区域突变(splice region/donor/acceptor variant)；对于同义突变(synonymous variant)、非编码区突变(UTR variant)、内含子突变(intron variant)不做报告。",paraStyle)
	flow_list.append(para)
	
	para=Paragraph(u"6.&nbsp; &nbsp;&nbsp;本结果已经过滤掉了千人基因组，ExAC03，ESP6500 等数据库中突变频率大于 5%的突变位点。",paraStyle)
	flow_list.append(para)
	
	para=Paragraph(u"7.&nbsp; &nbsp;&nbsp;本结果所用数据库版本：Human Genome hg19/GRCh37、RefSeq (release 61)、dbSNP (v144)、1000 Genomes phase3、esp6500、ExAC03。",paraStyle)
	flow_list.append(para)
	
	para=Paragraph(u"8.&nbsp; &nbsp;&nbsp;参考基因组是人类 hg19 版本。",paraStyle)
	flow_list.append(para)
	
	para=Paragraph(u"9.&nbsp; &nbsp;&nbsp;核心报告内容为本次检测得到的与所提供临床表型相关的致病或疑似致病位点，并进行了一代测序验证。",paraStyle)
	flow_list.append(para)
	
	para=Paragraph(u"10.&nbsp; &nbsp;&nbsp;扩展报告内容为本次检测得到的与所提供临床表型不符，但判读为致病或疑似致病的位点，未进行一代测序验证。",paraStyle)
	flow_list.append(para)
	return flow_list

##########################添加扩展报告内容##################################
def insertFifthPage():
	flow_list=[]
	paraStyle=setDefaultParagrahStyle()
	paraStyle.fontName="hei"
	paraStyle.fontSize=10
	paraStyle.spaceBefore = 5
	paraStyle.spaceAfter =2
	para=Paragraph(u"扩展报告内容：",paraStyle)
	flow_list.append(para)
	
	normalStyle=setDefaultParagrahStyle()
	normalStyle.fontSize=6
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
	extend_table=Table(extend_table_data,[0.55*inch,0.55*inch,0.65*inch,0.55*inch,0.4*inch,0.55*inch,0.55*inch,0.3*inch,0.55*inch,0.75*inch,0.55*inch,0.55*inch],[0.4*inch,0.5*inch,0.5*inch,0.5*inch,0.5*inch,0.5*inch,0.5*inch,0.5*inch,0.5*inch,0.5*inch,0.5*inch])
	extend_table.setStyle(TableStyle([
	('TOPPADDING',(0,0),(-1,-1),5),
	('LEFTPADDING',(0,0),(-1,-1),10),
	('LEADING',(0,0),(-1,-1),8),
	('ALIGN',(0,0),(-1,-1),'CENTER'),
	('BOX', (0,0), (-1,-1), 1, colors.black),
	('FONTNAME', (0,0), (-1,-1), 'hei'),
    ('FONTSIZE', (0,0), (-1,-1), 8),
	('VALIGN', (0,1), (-1,1), 'MIDDLE'),
	('FONTNAME', (0,1), (-1,-1), 'song'),
    ('FONTSIZE', (0,1), (-1,-1), 6),
	('INNERGRID', (0,0), (-1,-1), 0.5, colors.black)
	]))
	flow_list.append(extend_table)
	paraStyle=setDefaultParagrahStyle()
	paraStyle.fontName="song"
	paraStyle.fontSize=6
	paraStyle.spaceBefore =0
	paraStyle.spaceAfter =0
	paraStyle.leading=8
	para=Paragraph(u"注：该扩展报告内容为与检测过程中筛选的与临床表型不符的致病性或疑似致病性突变位点，经遗传模式、发病年龄、人群频率过滤，选择可能具有临床监控意义的位点报出，结果仅供临床参考。其中遗传模式缩写解释：AD 指常染色体显性遗传；AR 指常染色体隐性遗传；Mu:指多因子遗传。",paraStyle)
	flow_list.append(para)
	
	return flow_list  

#############################插入数据质控信息#############################
def insertSixthPage():
	flow_list=[]
	paraStyle=setDefaultParagrahStyle()
	paraStyle.fontName="hei"
	para=Paragraph(u'附件一.数据质控信息',paraStyle)
	flow_list.append(para)
	qc_table_data=[[u'样本名称',u'6E013'],[u'目标区域捕获效率',u'66.08%'],[u'目标区域覆盖度',u'97.25%'],[u'覆盖 4X 以上区域占比',u'96.79%'],[u'覆盖 20X 以上区域占比',u'95.22%'],[u'平均测序深度','113.10']]
	qc_table=Table(qc_table_data,2*[2*inch],6*[0.3*inch],hAlign="LEFT")
	qc_table.setStyle(TableStyle([
	('TOPPADDING',(0,0),(-1,-1),5),
	('LEFTPADDING',(0,0),(-1,-1),10),
	('LEADING',(0,0),(-1,-1),8),
	('ALIGN',(0,0),(-1,-1),'LEFT'),
	('BOX', (0,0), (-1,-1), 1, colors.black),
	('FONTNAME', (0,0), (-1,-1), 'hei'),
    ('FONTSIZE', (0,0), (-1,-1), 8),
	('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
	('INNERGRID', (0,0), (-1,-1), 0.5, colors.black)
	]))
	flow_list.append(qc_table)
	
	return flow_list

##########################结果渲染#################################################	
def renderPage():
	doc = SimpleDocTemplate("phello.pdf",pagesize=A4) 
	#-------------------first Page--------------------------------#
	Story.append(insertPageLogo())
	Story.append(Spacer(1, 2.2*inch))
	Story.append(insertClinicalAnnotation())
	Story.append(PageBreak())
	#-------------------second  Page-------------------------------#
	Story.append(insertPageLogo())
	Story.extend(insertSecondPage())
	Story.append(PageBreak())
	#------------------third Page---------------------------------#
	Story.append(insertPageLogo())
	Story.extend(insertThirdPage())
	Story.append(PageBreak())
	#---------------forth Page----------------------------------#
	Story.append(insertPageLogo())
	Story.extend(insertForthPage())
	Story.append(PageBreak())
	
	#---------------fifth Page-------------------------------#
	Story.append(insertPageLogo())
	Story.extend(insertFifthPage())
	Story.append(PageBreak())
	
	#--------------sixth Page---------------------------------#
	Story.append(insertPageLogo())
	Story.extend(insertSixthPage())
	Story.append(PageBreak())
	
	doc.build(Story,onFirstPage=myFirstPage,onLaterPages=myLaterPages)
	
if __name__ == "__main__":
   renderPage()