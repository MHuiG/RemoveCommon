# RemoveCommon

# 删除 python java C CPP JS CSS html xml  php sql 注释

## Python 

Python中的注释有单行注释和多行注释：

- 井号（#）

Python中单行注释以 # 开头，例如：

```
# 这是一个注释
print("Hello, World!")
多行注释用三个单引号 ''' 或者三个双引号 """ 将注释括起来，例如:
```

- 单引号（'''）

```
#!/usr/bin/python3 
'''
这是多行注释，用三个单引号
这是多行注释，用三个单引号 
这是多行注释，用三个单引号
'''
print("Hello, World!")
```

- 双引号（"""）
```
#!/usr/bin/python3 
"""
这是多行注释，用三个双引号
这是多行注释，用三个双引号 
这是多行注释，用三个双引号
"""
print("Hello, World!")
```

# java

- 单行注释	
```
// 注释内容
```
- 多行注释	

```
/*
... 注释内容....
... 注释内容....
... 注释内容....
*/
```

- 文档注释	

```
import java.io.*;
 
/**
* 这个类演示了文档注释
* @author Ayan Amhed
* @version 1.2
*/
public class SquareNum {
   /**
   * This method returns the square of num.
   * This is a multiline description. You can use
   * as many lines as you like.
   * @param num The value to be squared.
   * @return num squared.
   */
   public double square(double num) {
      return num * num;
   }
   /**
   * This method inputs a number from the user.
   * @return The value input as a double.
   * @exception IOException On input error.
   * @see IOException
   */
   public double getNumber() throws IOException {
      InputStreamReader isr = new InputStreamReader(System.in);
      BufferedReader inData = new BufferedReader(isr);
      String str;
      str = inData.readLine();
      return (new Double(str)).doubleValue();
   }
   /**
   * This method demonstrates square().
   * @param args Unused.
   * @return Nothing.
   * @exception IOException On input error.
   * @see IOException
   */
   public static void main(String args[]) throws IOException
   {
      SquareNum ob = new SquareNum();
      double val;
      System.out.println("Enter value to be squared: ");
      val = ob.getNumber();
      val = ob.square(val);
      System.out.println("Squared value is " + val);
   }
}
```


# C语言

- 以//开始、以换行符结束的单行注释
```
const double pi = 3.1415926536;       // pi是—个常量
```
- 以/*开始、以*/结束的块注释
```
int open( const char *name, int mode, … /* int permissions */ );
```

# html

- <!--...--> 标签

```
<!--这是一段注释。-->

<p>这是一段普通的段落。</p>
```

# php

- // 单行注释
```
// 单行注释
```
- 井号（#） 单行注释
```
 # 单行注释
```
- /* */多行注释块
```
/*
这是多行注释块
它横跨了
多行
*/
```
