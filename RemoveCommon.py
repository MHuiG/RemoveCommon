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
            print(Path)
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
    """Remover
    Attributes:
        Path: 文件路径
        Driver: 文件类型驱动
        OldFileLines: 原始文件
        MultilineComment: 多行注释列表
        RemoveComment: 需要删除的所有注释的行号列表
        Comment: 注释内容列表
        NoComment: 无注释内容列表
    """
    def __init__(self,Path,Driver):
        """Inits"""
        self.Path=Path
        self.Driver=Driver
        self.OldFileLines=list()
        self.MultilineComment=list()
        self.RemoveComment=list()
        self.Comment = list()
        self.NoComment = list()
        
    def run(self):
        """RUN"""
        self.ReadFile()
        self.RemoveComment = self.Driver.Handle(self)
        self.Handle()
        for i in self.Comment:
            print(i.encode("utf-8"))
        self.WriteFile()

    def ReadFile(self):
        """读取文件"""
        f = open(self.Path, "rb")
        OldFile = f.read().decode("utf8","ignore")
        f.close()
        self.OldFileLines = OldFile.splitlines()

    def Handle(self):
        """获取 注释和无注释 内容到列表中"""
        #去重并排序，得到所有注释行号的列表
        RemoveCommentNumber = sorted(set(self.RemoveComment))
        for i in RemoveCommentNumber:
            self.Comment.append(self.OldFileLines[i])
        # 创建与源文件总行号相同的列表 0,1,2,3...
        NewFileLines = list(i for i in range(len(self.OldFileLines)))
        # 删除注释的行号，留下无注释的行号 的列表集合
        for i in RemoveCommentNumber:
            NewFileLines.remove(i)
        for i in NewFileLines:
            self.NoComment.append(self.OldFileLines[i])

    def WriteFile(self):
        """写入文件"""
        with open(self.Path,"wb") as f:
            for i in self.NoComment:
                i=self.Driver.CheckLine(i)
                i=self.Driver.CheckOne(i)
                f.write(i.encode("utf-8"))
                f.write("\n".encode("utf-8"))
                
class Driver(object):
    """Driver
    Attributes:
        OldFileLines: 原始文件
        MultilineComment: 多行注释列表
        RemoveComment: 需要删除的所有注释的行号列表
        flag: 标记
    """
    def __init__(self):
        """Inits"""
        self.OldFileLines=list()
        self.MultilineComment=list()
        self.RemoveComment=list()
        self.flag=0
        
    def Handle(self,Remover):
        """处理"""
        self.OldFileLines=Remover.OldFileLines
        i = 0
        for line in self.OldFileLines:
            # Remove 空行以及全是空格的行
            ret_0 = re.match(r"^[\s]*$",line)
            if ret_0:
                self.RemoveComment.append(i)
            self.Check(line,i)
            i=i+1

        # 将两个多行注释行号之间所有的行添加到 # 号列表中
        while self.MultilineComment != []:
            # 从列表中移出最后两个元素
            a = self.MultilineComment.pop()
            b = self.MultilineComment.pop()
            temp = b
            while temp <= a:
                self.RemoveComment.append(temp)
                temp += 1
        # 返回需要删除的所有注释的 行号 集合
        return self.RemoveComment

    def CheckOne(self,s):
        """Remove空行"""
        a=re.compile("^[\s]*$")
        if a.findall(s):
            print(a.findall(s))
            t=a.sub("",s)
            return t
        return s

    def Check(self,line,i):
        """Check"""
        pass
    
    def CheckLine(self,s):
        """CheckLine"""
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
        # 符号 =""" 独占一行 pass
        ret_2 = re.match(r".*=[\sr]*\"\"\".*",line)
        if ret_2:
            #print(line)
            self.flag=1
        # 符号 # XXX""" 独占一行 pass
        ret_2 = re.match(r".*#.*\"\"\".*",line)
        if ret_2:
            #print(line)
            self.flag=1
        # """....""" pass
        a=re.compile("\"\"\".*\"\"\"")
        b=re.compile("=[r\s]*\"\"\".*\"\"\"")
        # =""" pass
        c=re.compile(".*=[\sr]*\"\"\".*")
        
        if  (len(a.findall(line))==0)&(len(b.findall(line))==0)&(len(c.findall(line))==0):
            # 符号 """XXXXX or """独占一行 add
            ret_2 = re.match(r"[\sr]*(?!\=.*)\"\"\"(?!.*\"\"\")",line)
            if ret_2:
                if self.flag==0:
                    #print(line)
                    self.MultilineComment.append(i)
                if self.flag==1:
                    #print(line)
                    self.flag=0
            else:
                # 符号 XXXX""" 独占一行 add
                ret_3 = re.match(r".*\"\"\"",line)
                if ret_3:
                        if self.flag==0:
                            #print(line)
                            self.MultilineComment.append(i)
                        if self.flag==1:
                            #print(line)
                            self.flag=0
           
    def CheckLine(self,s):
        # 符号 #
        a=re.compile("#(?!!)(?!.*-\*-)(?!.*\')(?!.*\")(?!.*\"\"\").*")
        if a.findall(s):
            print(a.findall(s))
            t=a.sub("",s)
            return t
        # 符号 """...."""
        a=re.compile("\"\"\".*\"\"\"")
        b=re.compile("=[r\s]*\"\"\".*\"\"\"")
        if (len(a.findall(s))!=0)&(len(b.findall(s))==0):
            print(a.findall(s))
            t=a.sub("",s)
            return t
        return s

class HTML(Driver):
    def Check(self,line,i):
        # 符号 <!-- XXXXXX -->独占一行 add
        ret_1 = re.match(r"^[^\w]*<!--.*-->",line)
        if ret_1:
            #print(line)
            self.RemoveComment.append(i)
        #   <!-- XXXXXX --> pass [for <!-- XXXXXX & XXXXXX -->]
        a=re.compile("<!--.*-->")
        # XXXXXX <!--  pass
        ret_2 = re.match(".*>[\s]*<!--(?!.*-->).*",line)
        if ret_2:
            #print(line)
            self.MultilineComment.append(i+1)
        # 符号 <!-- XXXXXX 独占一行 add
        ret_2 = re.match(r"^[\s]*<!--.*",line)
        if ret_2:
            if len(a.findall(line))==0:
                #print(line)
                self.MultilineComment.append(i)
        # 符号 XXXXXX --> 独占一行 add
        ret_2 = re.match(r".*-->",line)
        if ret_2:
            if len(a.findall(line))==0:
                #print(line)
                self.MultilineComment.append(i)

    def CheckLine(self,s):
        # 符号 <!-- XXXXXX -->
        a=re.compile("<!--.*-->")
        if a.findall(s):
            print(a.findall(s))
            t=a.sub("",s)
            return t
        # 符号 <!-- XXXXXX
        a=re.compile("<!--.*")
        if a.findall(s):
            print(a.findall(s))
            t=a.sub("",s)
            return t
        # 符号 XXXXXX  -->
        a=re.compile(".*-->")
        if a.findall(s):
            print(a.findall(s))
            t=a.sub("",s)
            return t
        return s

   
class C(Driver):
    def Check(self,line,i):
        # 符号 /* XXXXXX */独占一行 add
        ret_1 = re.match(r"^[^\w]*/\*.*\*/",line)
        if ret_1:
            #print(line)
            self.RemoveComment.append(i)
        #   /* XXXXXX */ pass [for /* XXXXXX & XXXXXX */]
        a=re.compile("/\*.*\*/")
        #  " /* " pass
        b=re.compile("[\'\"].*/\*.*[\'\"]")
        if (len(a.findall(line))==0) and (len(b.findall(line))==0):
            # XXXXXX /*  pass NEXT
            ret_2 = re.match("^[^\s].*/\*.*",line)
            if ret_2:
                #print(line)
                self.MultilineComment.append(i+1)
            # 符号 /* XXXXXX 独占一行 add
            ret_2 = re.match(r"^[\s]*/\*.*",line)
            if ret_2:
                #print(line)
                self.MultilineComment.append(i)
            # 符号 XXXXXX */ 独占一行 add
            ret_2 = re.match(r".*\*/",line)
            if ret_2:
                #print(line)
                self.MultilineComment.append(i)
    
    def CheckLine(self,s):
        # 符号 //
        a=re.compile("//(?!.*\')(?!.*\").*")
        if a.findall(s):
            print(a.findall(s))
            t=a.sub("",s)
            return t
        # 符号 /* XXXXXX */
        a=re.compile("/\*.*\*/(?!.*\')(?!.*\")")
        if a.findall(s):
            print(a.findall(s))
            t=a.sub("",s)
            return t
        # 符号 /* XXXXXX
        a=re.compile("/\*(?!.*\')(?!.*\").*")
        if a.findall(s):
            print(a.findall(s))
            t=a.sub("",s)
            return t
        # 符号 XXXXXX  */
        a=re.compile(".*\*/(?!.*\')(?!.*\")")
        if a.findall(s):
            print(a.findall(s))
            t=a.sub("",s)
            return t
        return s
 
if __name__=="__main__":
    
    FilePath="./File/"
    walkFile(FilePath)

