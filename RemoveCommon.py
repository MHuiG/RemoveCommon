#-*- coding: utf-8 -*-
import os
import re

def walkFile(FilePath):
    """walkFile
    Traversal folder file matching file extension
    Args:
        FilePath: 文件路径
    """
    for root, dirs, files in os.walk(FilePath):
        for f in files:
            Path=os.path.join(root, f)
            print(Path)
            if os.path.splitext(f)[1] in [".py"]:
                driver=PY()
                Remover(Path,driver).run()
            if os.path.splitext(f)[1] in [".java",".c",".cpp",".h",".js",".css"]:
                driver=C()
                Remover(Path,driver).run()
            if os.path.splitext(f)[1] in [".html",".xml"]:
                driver=HTML()
                Remover(Path,driver).run()
                driver=C()
                Remover(Path,driver).run()
            if os.path.splitext(f)[1] in [".php"]:
                driver=PHP()
                Remover(Path,driver).run()
            if os.path.splitext(f)[1] in [".sql"]:
                driver=SQL()
                Remover(Path,driver).run()


class Remover(object):
    """Remover过滤器
    注释行号列表=RemoveSort(RemoveSort(单行注释行号列表+多行注释行号列表)-RemoveSort(例外单行注释行号列表+例外多行注释行号列表))
    RCN=RemoveSort(RemoveSort(TN)-RemoveSort(FN))
    Attributes:
        Path: 文件路径
        Driver: 文件类型驱动
        OldFileLines: 原始文件行列表
        Comment: 注释内容列表
        NoComment: 无注释内容列表
    """
    def __init__(self,Path,Driver):
        """初始化"""
        self.Path=Path
        self.Driver=Driver
        self.OldFileLines=list()
        self.Comment = list()
        self.NoComment = list()
        
    def run(self):
        """RUN"""
        try:
            self.ReadFile()
            self.RemoverHandle()
            self.PrintComment()
            print("===============================")
            #self.PrintNoComment()
            #self.WriteFile()
        except Exception as e:
            print(self.Path)
            print(e)
            self.ERRORHandle()
    def ReadFile(self):
        """读取文件"""
        f = open(self.Path, "rb")
        OldFile = f.read().decode("utf8","ignore")
        f.close()
        self.OldFileLines = OldFile.splitlines()

    def RemoverHandle(self):
        """过滤处理"""
        self.Driver.NumberDriverHandle(self.OldFileLines)
        RemoveCommentNumber=sorted(set(self.Driver.TN)-set(self.Driver.FN))
        for i in RemoveCommentNumber:
            self.Comment.append(self.OldFileLines[i])
        NewFileLines = list(i for i in range(len(self.OldFileLines)))
        for i in RemoveCommentNumber:
            NewFileLines.remove(i)
        for i in NewFileLines:
            self.Driver.LineDriverHandle(self.OldFileLines[i])
            self.NoComment.append(self.Driver.newline)

    def WriteFile(self):
        """写入文件"""
        with open(self.Path,"wb") as f:
            for i in self.NoComment:
                f.write(i.encode("utf-8"))
                f.write("\n".encode("utf-8"))

    def PrintComment(self):
        """打印注释"""
        for i in self.Comment:
            print(i.encode("utf-8"))
            #print(i)
            
    def PrintNoComment(self):
        """打印非注释"""
        for i in self.NoComment:
            print(i.encode("utf-8"))
            #print(i)
            
    def ERRORHandle(self):
        """异常处理"""
        try:
            os.mkdir(".ERROR/")
        except:
            pass
        try:
            import shutil
            shutil.copy(self.Path,".ERROR/")
        except:
            pass

class Driver(object):
    """Driver过滤器驱动
    Attributes:
        OldFileLines: 原始文件
        TN: 临时注释行号列表
        FN: 例外注释行号列表
        line: 当前行
        newline: 新行
        i: 当前行号
        flag: 标记
        flage: 例外标记
    """
    def __init__(self):
        """初始化"""
        self.OldFileLines=list()
        self.TN=list()
        self.FN=list()
        self.line=""
        self.newline=""
        self.i=0
        self.flag=0
        self.flage=0
        
    def NumberDriverHandle(self,OldFileLines):
        """行号过滤器驱动处理
            将两个多行注释行号之间所有的行添加到 # 号列表中
        Args:
            OldFileLines: 原始文件
        """
        self.OldFileLines=OldFileLines
        self.i=0
        for line in self.OldFileLines:
            self.line=line
            if self.flag==1:
                self.TN.append(self.i)
            if self.flage==1:
                self.FN.append(self.i)
            self.NumberDriver()
            self.i=self.i+1

    def LineDriverHandle(self,line):
        """行值过滤器驱动处理
            处理单行
        Args:
            line: 原始行值
        """
        self.flag=0
        self.flage=0
        self.line=line
        self.LineDriver()


    def SNR(self,s):
        """单行注释行号过滤规则"""
        if re.match(s,self.line):
            self.TN.append(self.i)

    def MNR(self,l,r):
        """多行注释行号过滤规则"""
        if re.match(l,self.line) and self.flag==0:
            self.flag=1
            self.TN.append(self.i)
            return
        if re.match(r,self.line) and self.flag==1:
            self.flag=0
            return

    def ESNR(self,s):
        """例外单行注释行号过滤规则"""
        if re.match(s,self.line):
            self.FN.append(self.i)

    def EMNR(self,l,r):
        """例外多行注释行号过滤规则"""
        if re.match(l,self.line):
            self.flage=1
            self.FN.append(self.i)
            return
        if re.match(r,self.line):
            self.flage=0
            return

    def LR(self,s):
        """注释行值过滤规则"""
        if self.flag==0:
            self.newline=self.line
        if self.flage==0:
            a=re.compile(s)
            if a.findall(self.line):
                print(a.findall(self.line))
                self.newline=a.sub("",self.line)
                if self.flag==0:
                    self.flag=1
        else:
            self.flage=0
                
    def ELR(self,s):
        """例外注释行值过滤规则
            ELR() needs to be before LR()
            one or more ELR() 只对一个 LR() work
        """
        a=re.compile(s)
        if a.findall(self.line):
            self.flage=1


    def NumberDriver(self):
        """Line number filter drive logic
        self.SNR()
        self.MNR()
        self.ESNR()
        self.EMNR()
        """
        pass
    
    def LineDriver(self):
        """Row value filter drive logic
        Waring: only one LR() work for each line
                ELR() needs to be before LR()
                one or more ELR() work for only one LR() 

            self.ELR()
            self.LR()
            
            self.ELR()
            self.ELR()
            self.LR()
        """
        self.newline=self.line



    
class PY(Driver):
    def NumberDriver(self):
        # Remove 空行
        self.SNR("^[\s]*$")
        # Remove # 独占一行
        self.SNR("^[^\w]*#+")
        # Pass #-*- coding: utf-8 -*-
        self.ESNR("#.*coding")
        # Pass #!env
        self.ESNR("#!")
        # Remove """....""" 独占一行
        self.SNR("^[^\w]*\"\"\".*\"\"\"")
        # Remove '''....''' 独占一行
        self.SNR("^[^\w]*\'\'\'.*\'\'\'")
        # Remove """....""" 多行
        self.MNR("^[^#\"\']*\"\"\"(?!.*\"\"\")","((?!#)(?!\"\"\").)*\"\"\"(?!.*\"\"\")")
        # Pass ="""
        self.EMNR("^[^#\"\']*=[r\s]*\"\"\"","((?!#)(?!\"\"\").)*\"\"\"(?!.*\"\"\")")
        # Remove '''....''' 多行
        self.MNR("^[^#\"\']*\'\'\'(?!.*\'\'\')","((?!#)(?!\'\'\').)*\'\'\'(?!.*\'\'\')")
        # Pass ='''
        self.EMNR("^[^#\"\']*=[r\s]*\'\'\'","((?!#)(?!\'\'\').)*\'\'\'(?!.*\'\'\')")
        # Pass XXXX  """ .....
        self.ESNR(".*[\d\w\t]{1,}\"\"\"")
        
    def LineDriver(self):
        # Pass #!env
        self.ELR("#!.*")
        # Pass #-*- coding: utf-8 -*-
        self.ELR("#.*coding:")
        # Pass '#'
        self.ELR("\'.*#.*\'")
        # Pass "#"
        self.ELR("\".*#.*\"")
        # Pass '''#'''
        self.ELR("\'\'\'.*#.*\'\'\'")
        # Pass """#"""
        self.ELR("\"\"\".*#.*\"\"\"")
        # Remove #
        self.LR("#.*")
        # Pass =""" ...
        self.ELR("^[^#\"\']*=[r\s]*\"\"\"")
        # Remove """...."""
        self.LR("^[^#\"\']*\"\"\".*\"\"\"")
        # Remove '''....'''
        self.LR("^[^#\"\']*\'\'\'.*\'\'\'")
        # Pass =""" ...
        self.ELR("^[^#\"\']*=[r\s]*\"\"\"")
        # Pass """ 独占一行
        self.ELR("^[^\w]*\"\"\".*")
        # Remove ..."""
        self.LR("^[^#\"\']*\"\"\".*")
        # Pass =''' ...
        self.ELR("^[^#\"\']*=[r\s]*\'\'\'")
        # Pass ''' 独占一行
        self.ELR("^[^\w]*\'\'\'.*")
        # Remove ...'''
        self.LR("^[^#\"\']*\'\'\'.*")

        
class HTML(Driver):
    def NumberDriver(self):
        # Remove 空行
        self.SNR("^[\s]*$")
        # Remove <!-- XXXXXX -->独占一行
        self.SNR("^[^\w]*<!--.*-->")
        # Pass <!-- XXXXXX --> 单行 [for <!-- XXXXXX & XXXXXX -->]
        self.ESNR("<!--.*-->")
        # Remove  <!-- XXXXXX --> 多行
        self.MNR(".*<!--(?!.*-->).*","((?!<!--).)*-->")
        # Pass XXXXXX <!--
        self.ESNR(".*>[\s]*<!--(?!.*-->).*")
        # Pass XXXXXX -->
        self.ESNR("((?!<!--).)*-->.*")
        # Pass <!--[if lt IE 9]><![endif]-->
        self.ESNR("<!--.*[if.*].*>.*<!.*[.*endif.*].*-->")
        # Pass <!--[if lt IE 9]>
        self.ESNR("<!--.*[if.*].*>")
        # Pass <![endif]-->
        self.ESNR("<!.*[.*endif.*].*-->")

        
    def LineDriver(self):
        # Pass <!--[if lt IE 9]><![endif]-->
        self.ELR("<!--.*[if.*].*>.*<!.*[.*endif.*].*-->")
        # Pass <!--[if lt IE 9]>
        self.ELR("<!--.*[if.*].*>")
        # Pass <![endif]-->
        self.ELR("<!.*[.*endif.*].*-->")
        # Remove <!-- XXXXXX -->
        self.LR("<!--.*-->")
        # Pass <!--[if lt IE 9]><![endif]-->
        self.ELR("<!--.*[if.*].*>.*<!.*[.*endif.*].*-->")
        # Pass <!--[if lt IE 9]>
        self.ELR("<!--.*[if.*].*>")
        # Remove <!-- XXXXXX
        self.LR("<!--(?!.*-->).*")
        # Pass <!--[if lt IE 9]><![endif]-->
        self.ELR("<!--.*[if.*].*>.*<!.*[.*endif.*].*-->")
        # Pass <![endif]-->
        self.ELR("<!.*[.*endif.*].*-->")
        # Remove XXXXXX  -->
        self.LR("((?!<!--).)*-->")

class C(Driver):
    def NumberDriver(self):
        # Remove 空行
        self.SNR("^[\s]*$")
        # Remove /* XXXXXX */独占一行
        self.SNR("^[^\w]*/\*.*\*/")
        # Remove  /* XXXXXX */ 多行
        self.MNR(".*/\*(?!.*\*/).*","((?!/\*).)*\*/")
        # Pass XXXXXX /*
        self.ESNR(".*/\*.*")
        
    def LineDriver(self):
        # Pass '//'
        self.ELR("\'.*//.*\'")
        # Pass "//"
        self.ELR("\".*//.*\"")
        # Remove //
        self.LR("//.*")
        # Pass '/* XXXXXX */'
        self.ELR("\'.*/\*.*\*/.*\'")
        # Pass "/* XXXXXX */"
        self.ELR("\".*/\*.*\*/.*\"")
        # Remove /* XXXXXX */
        self.LR("/\*.*\*/")
        # Pass '/* XXXXXX'
        self.ELR("\'/\*.*\'")
        # Pass "/* XXXXXX"
        self.ELR("\"/\*.*\"")
        # Remove /* XXXXXX
        self.LR("/\*(?!.*\*/).*")
        # Pass 'XXXXXX*/'
        self.ELR("\'.*\*/\'")
        # Pass "XXXXXX*/"
        self.ELR("\".*\*/\"")

class SQL(Driver):
    def NumberDriver(self):
        # Remove 空行
        self.SNR("^[\s]*$")
        # Remove /* XXXXXX */独占一行
        self.SNR("^[^\w]*/\*.*\*/")
        # Remove  /* XXXXXX */ 多行
        self.MNR(".*/\*(?!.*\*/).*","((?!/\*).)*\*/")
        # Pass XXXXXX /*
        self.ESNR(".*/\*.*")
        
    def LineDriver(self):
        # Pass '--'
        self.ELR("\'.*--.*\'")
        # Pass "--"
        self.ELR("\".*--.*\"")
        # Remove --
        self.LR("--.*")
        # Pass '/* XXXXXX */'
        self.ELR("\'.*/\*.*\*/.*\'")
        # Pass "/* XXXXXX */"
        self.ELR("\".*/\*.*\*/.*\"")
        # Pass /*! XXXXXX */;
        self.ELR("/\*!.*\*/;")
        # Remove /* XXXXXX */
        self.LR("/\*.*\*/")
        # Pass '/* XXXXXX'
        self.ELR("\'.*/\*.*\'")
        # Pass "/* XXXXXX"
        self.ELR("\".*/\*.*\"")
        # Remove /* XXXXXX
        self.LR("/\*(?!.*\*/).*")
        # Pass 'XXXXXX*/'
        self.ELR("\'.*\*/.*\'")
        # Pass "XXXXXX*/"
        self.ELR("\".*\*/.*\"")

class PHP(Driver):
    def NumberDriver(self):
        # Remove 空行
        self.SNR("^[\s]*$")
        # Remove # 独占一行
        self.SNR("^[^\w]*#+")
        # Remove /* XXXXXX */独占一行
        self.SNR("^[^\w]*/\*.*\*/")
        # Remove  /* XXXXXX */ 多行
        self.MNR(".*/\*(?!.*\*/).*","((?!/\*).)*\*/")
        # Pass XXXXXX /*
        self.ESNR(".*/\*.*")
        
    def LineDriver(self):
        # Pass '#'
        self.ELR("\'.*#.*\'")
        # Pass "#"
        self.ELR("\".*#.*\"")
        # Pass '''#'''
        self.ELR("\'\'\'.*#.*\'\'\'")
        # Pass """#"""
        self.ELR("\"\"\".*#.*\"\"\"")
        # Remove #
        self.LR("#.*")
        # Pass '//'
        self.ELR("\'.*//.*\'")
        # Pass "//"
        self.ELR("\".*//.*\"")
        # Remove //
        self.LR("//.*")
        # Pass '/* XXXXXX */'
        self.ELR("\'.*/\*.*\*/.*\'")
        # Pass "/* XXXXXX */"
        self.ELR("\".*/\*.*\*/.*\"")
        # Remove /* XXXXXX */
        self.LR("/\*.*\*/")
        # Pass '/* XXXXXX'
        self.ELR("\'/\*.*\'")
        # Pass "/* XXXXXX"
        self.ELR("\"/\*.*\"")
        # Remove /* XXXXXX
        self.LR("/\*(?!.*\*/).*")
        # Pass 'XXXXXX*/'
        self.ELR("\'.*\*/.*\'")
        # Pass "XXXXXX*/"
        self.ELR("\".*\*/.*\"")




if __name__=="__main__":
    
    FilePath="./File/"
    walkFile(FilePath)

