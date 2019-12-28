#-*- coding: utf-8 -*-
import os
import re

def walkFile(FilePath):
    """walkFile
    遍历文件夹文件 匹配文件扩展名
    Args:
        FilePath: 文件路径
    """
    for root, dirs, files in os.walk(FilePath):
        for f in files:
            Path=os.path.join(root, f)
            #print(Path)
            if os.path.splitext(f)[1] in [".py"]:
                driver=PY()
                Remover(Path,driver).run()
            if os.path.splitext(f)[1] in [".java",".c",".cpp",".h",".js",".css"]:
                driver=C()
                Remover(Path,driver).run()
            if os.path.splitext(f)[1] in [".html"]:
                driver=HTML()
                Remover(Path,driver).run()

class Remover(object):
    """Remover过滤器
    Attributes:
        Path: 文件路径
        Driver: 文件类型驱动
        OldFileLines: 原始文件行列表
        RemoveComment: 需要删除的所有注释的行号列表
        Comment: 注释内容列表
        NoComment: 无注释内容列表
    """
    def __init__(self,Path,Driver):
        """初始化"""
        self.Path=Path
        self.Driver=Driver
        self.OldFileLines=list()
        self.RemoveComment=list()
        self.Comment = list()
        self.NoComment = list()
        
    def run(self):
        """RUN"""
        try:
            self.ReadFile()
            self.RemoverHandle()
            #self.PrintComment()
            self.WriteFile()
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
        self.RemoveComment = self.Driver.DriverHandle(self.OldFileLines)
        RemoveCommentNumber = sorted(set(self.RemoveComment))
        for i in RemoveCommentNumber:
            self.Comment.append(self.OldFileLines[i])
        NewFileLines = list(i for i in range(len(self.OldFileLines)))
        for i in RemoveCommentNumber:
            NewFileLines.remove(i)
        for i in NewFileLines:
            temp=self.OldFileLines[i]
            temp=self.Driver.CheckLine(temp)
            temp=self.Driver.CheckOne(temp)
            self.NoComment.append(temp)

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
        MultilineComment: 多行注释列表
        RemoveComment: 需要删除的所有注释的行号列表
        flag: 标记
    """
    def __init__(self):
        """初始化"""
        self.OldFileLines=list()
        self.MultilineComment=list()
        self.RemoveComment=list()
        self.flag=0
        
    def DriverHandle(self,OldFileLines):
        """过滤器驱动处理
            将两个多行注释行号之间所有的行添加到 # 号列表中
        Args:
            OldFileLines: 原始文件
        return:
            需要删除的所有注释的 行号 集合
        """
        self.OldFileLines=OldFileLines
        i = 0
        for line in self.OldFileLines:
            # Remove 空行
            ret_0 = re.match(r"^[\s]*$",line)
            if ret_0:
                self.RemoveComment.append(i)
            self.Check(line,i)
            i=i+1
        while self.MultilineComment != []:
            a = self.MultilineComment.pop()
            b = self.MultilineComment.pop()
            temp = b
            while temp <= a:
                self.RemoveComment.append(temp)
                temp += 1
        return self.RemoveComment

    def CheckOne(self,s):
        """移除空行(单行检查规则)"""
        a=re.compile("^[\s]*$")
        if a.findall(s):
            #print(a.findall(s))
            t=a.sub("",s)
            return t
        return s

    def Check(self,line,i):
        """多行检查规则
        Args:
            line: 原始文件行
            i: line所对应的行号
        """
        pass
    
    def CheckLine(self,s):
        """单行检查Remove规则
        Args:
            s: 原始文件行
        return:
            处理后的行
        """
        return s

class PY(Driver):
    def Check(self,line,i):
        # Remove # 独占一行
        ret_1 = re.match(r"^[^\w]*#+",line)
        ret_1_2 = re.match(r"#.*-\*-",line)
        ret_1_3 = re.match(r"#!",line)
        if ret_1_2:
            pass
        elif ret_1_3:
            pass
        elif ret_1:
            self.RemoveComment.append(i)
        # Pass """....""" 
        a=re.compile("\"\"\".*\"\"\"")
        b=re.compile("=[r\s]*\"\"\".*\"\"\"")
        # Pass ="""
        c=re.compile(".*=[\sr]*\"\"\".*")
        # Pass =""" 独占一行
        ret_2 = re.match(r".*=[\sr]*\"\"\".*",line)
        if ret_2:
            #print(line)
            self.flag=1
        if  (len(a.findall(line))==0)&(len(b.findall(line))==0)&(len(c.findall(line))==0):
            # Pass # XXX""" 独占一行
            ret_2 = re.match(r".*#.*\"\"\".*",line)
            if ret_2:
                #print(line)
                self.flag=1
            # Remove """XXXXX 独占一行
            ret_2 = re.match(r"[\sr]*(?!\=.*)\"\"\"(?!.*\"\"\")",line)
            if ret_2:
                if self.flag==0:
                    #print(line)
                    self.MultilineComment.append(i)
                if self.flag==1:
                    #print(line)
                    self.flag=0
            else:
                # Remove XXXX""" 独占一行
                ret_3 = re.match(r".*\"\"\"(?!.*\")(?!.*\')",line)
                if ret_3:
                        if self.flag==0:
                            #print(line)
                            self.MultilineComment.append(i)
                        if self.flag==1:
                            #print(line)
                            self.flag=0
           
    def CheckLine(self,s):
        # Remove #
        a=re.compile("#(?!!)(?!.*-\*-)(?!.*\')(?!.*\")(?!.*\"\"\").*")
        if a.findall(s):
            #print(a.findall(s))
            t=a.sub("",s)
            return t
        # Remove """...."""
        a=re.compile("\"\"\".*\"\"\"")
        b=re.compile("=[r\s]*\"\"\".*\"\"\"")
        if (len(a.findall(s))!=0)&(len(b.findall(s))==0):
            #print(a.findall(s))
            t=a.sub("",s)
            return t
        return s

class HTML(Driver):
    def Check(self,line,i):
        # Remove <!-- XXXXXX -->独占一行
        ret_1 = re.match(r"^[^\w]*<!--.*-->",line)
        if ret_1:
            #print(line)
            self.RemoveComment.append(i)
        # Pass <!-- XXXXXX -->  [for <!-- XXXXXX & XXXXXX -->]
        a=re.compile("<!--.*-->")
        if len(a.findall(line))==0:
            # Pass XXXXXX <!--
            ret_2 = re.match(".*>[\s]*<!--(?!.*-->).*",line)
            if ret_2:
                #print(line)
                self.MultilineComment.append(i+1)
            # Remove <!-- XXXXXX 独占一行 
            ret_2 = re.match(r"^[\s]*<!--.*",line)
            if ret_2:
                #print(line)
                self.MultilineComment.append(i)
            # Remove XXXXXX --> 独占一行 
            ret_2 = re.match(r".*-->",line)
            if ret_2:
                #print(line)
                self.MultilineComment.append(i)

    def CheckLine(self,s):
        # Remove <!-- XXXXXX -->
        a=re.compile("<!--.*-->")
        if a.findall(s):
            #print(a.findall(s))
            t=a.sub("",s)
            return t
        # Remove <!-- XXXXXX
        a=re.compile("<!--.*")
        if a.findall(s):
            #print(a.findall(s))
            t=a.sub("",s)
            return t
        # Remove XXXXXX  -->
        a=re.compile(".*-->")
        if a.findall(s):
            #print(a.findall(s))
            t=a.sub("",s)
            return t
        return s

   
class C(Driver):
    def Check(self,line,i):
        # Remove /* XXXXXX */独占一行
        ret_1 = re.match(r"^[^\w]*/\*.*\*/",line)
        if ret_1:
            #print(line)
            self.RemoveComment.append(i)
        # Pass  /* XXXXXX */  [for /* XXXXXX & XXXXXX */]
        a=re.compile("/\*.*\*/")
        # Pass " /* " 
        b=re.compile("[\'\"].*/\*.*[\'\"]")
        # Pass " */ "
        c=re.compile("[\'\"].*\*/.*[\'\"]")
        if (len(a.findall(line))==0) and (len(b.findall(line))==0)and (len(c.findall(line))==0):
            # Pass XXXXXX /* XXXXXX  & Remove NEXT
            ret_2 = re.match("^[^\s].*/\*.*",line)
            if ret_2:
                #print(line)
                self.MultilineComment.append(i+1)
            # Remove /* XXXXXX 独占一行
            ret_2 = re.match(r"^[\s]*/\*.*",line)
            if ret_2:
                #print(line)
                self.MultilineComment.append(i)
            # Remove XXXXXX */ 独占一行
            ret_2 = re.match(r".*\*/",line)
            if ret_2:
                #print(line)
                self.MultilineComment.append(i)
    
    def CheckLine(self,s):
        # Remove //
        a=re.compile("//(?!.*\')(?!.*\").*")
        if a.findall(s):
            #print(a.findall(s))
            t=a.sub("",s)
            return t
        # Remove // "XXX"
        a=re.compile("//.*\".*\".*")
        if a.findall(s):
            #print(a.findall(s))
            t=a.sub("",s)
            return t
        # Remove // 'XXX'
        a=re.compile("//.*\'.*\'.*")
        if a.findall(s):
            #print(a.findall(s))
            t=a.sub("",s)
            return t
        # Remove /* XXXXXX */
        a=re.compile("/\*.*\*/(?!.*\')(?!.*\")")
        if a.findall(s):
            #print(a.findall(s))
            t=a.sub("",s)
            return t
        # Remove /* XXXXXX
        a=re.compile("/\*(?!.*\')(?!.*\").*")
        if a.findall(s):
            #print(a.findall(s))
            t=a.sub("",s)
            return t
        # Remove XXXXXX */
        a=re.compile(".*\*/(?!.*\')(?!.*\")")
        if a.findall(s):
            #print(a.findall(s))
            t=a.sub("",s)
            return t
        return s
 
if __name__=="__main__":
    
    FilePath="./File/"
    walkFile(FilePath)

