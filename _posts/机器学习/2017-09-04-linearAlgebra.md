---
layout: post
title:  "线性代数"
date:   2017-09-04
desc: "Machine learn linear algebra"
keywords: "机器学习,python,线性代数"
categories: [Machinelearn]
tags: [机器学习,python,线性代数]
icon: icon-python
---

## 矩阵
1. 3*2 矩阵,\\(A_{ij}  \\)  第i行，第j列元素
$$
A=
  \begin{bmatrix}
        1 \quad x^2 \\
        2 \quad y^2 \\
        3 \quad z^2 
  \end{bmatrix} \tag{1}
  $$

2. 向量是特殊的矩阵，3维列向量 
$$
y=
 \left[
 \begin{matrix}
   1  \\
   4  \\
   7 
  \end{matrix}
  \right] \tag{2}
$$

##  加法和标量乘法   

1. 矩阵的加法：行列数相等的可以加  
$$
  \begin{bmatrix}
        1 \quad 0 \\
        2 \quad 5 \\
        3 \quad 1 
  \end{bmatrix}
  $$  +
$$
  \begin{bmatrix}
        4 \quad 0.5 \\
        2 \quad 5 \\
        0 \quad 1 
  \end{bmatrix} 
  $$  =
$$
  \begin{bmatrix}
        5 \quad 0.5 \\
        4 \quad 10 \\
        3 \quad 2 
  \end{bmatrix} 
  $$

2. 矩阵的乘法：每个元素都要乘  
3 *
$$
  \begin{bmatrix}
        1 \quad 0 \\
        2 \quad 5 \\
        3 \quad 1 
  \end{bmatrix} 
$$ =
$$
  \begin{bmatrix}
        3 \quad 0 \\
        6 \quad 15 \\
        9 \quad 3 
  \end{bmatrix} 
  $$ =
$$
  \begin{bmatrix}
        1 \quad 0 \\
        2 \quad 5 \\
        3 \quad 1 
  \end{bmatrix} 
  $$ * 3

3. 矩阵向量乘法: m*n 矩阵* n*1 矩阵= m*1 矩阵  
$$
  \begin{bmatrix}
        1 \quad 3 \\
        4 \quad 0 \\
        2 \quad 1 
  \end{bmatrix} 
  $$
  $$
  \begin{bmatrix}
        1  \\        
        5 
  \end{bmatrix} 
  $$=
  $$
  \begin{bmatrix}
        16 \\
        4 \\
        7
  \end{bmatrix} 
  $$  

    1 * 1+3 * 5=16  
    4 * 1+0 * 5=4  
    2 * 1=1 * 5=7  

4. m * n 矩阵乘以 n * o 矩阵，变成 m * o 矩阵  
$$
  \begin{bmatrix}
        Co \quad C1 \\
        C2 \quad C3 
  \end{bmatrix} 
$$ =
$$
  \begin{bmatrix}
        Ao \quad A1 \\
        A2 \quad A3 
  \end{bmatrix} 
  $$  *
$$
  \begin{bmatrix}
        Bo \quad B1 \\
        B2 \quad B3 
  \end{bmatrix} 
  $$ 

    C0=A0 * B0 + A1 * B2  
    C1=A0 * B1 + A1 * B3  
    C0=A2 * B0 + A3 * B2  
    C0=A2 * B1 + A3 * B3  
5.  矩阵乘法性质  
  矩阵的乘法不满足交换律：A×B≠B×A  
  矩阵的乘法满足结合律。即：A×（B×C）=（A×B）×C  
  单位矩阵：在矩阵的乘法中，有一种矩阵起着特殊的作用，如同数的乘法中的 1,我们称
    这种矩阵为单位矩阵．它是个方阵，一般用 I 或者 E表示,从左上角到右下角的对角线（称为主对角线）上的元素均为 1 以外全都为 0  
    $$
      \begin{bmatrix}
            1 \quad 0 \\
            0 \quad 1 
      \end{bmatrix} 
    $$ 
  AI=IA=A  

6. 逆、转置  
  矩阵的逆：如矩阵 A 是一个 m×m 矩阵（方阵），如果有逆矩阵，则：\\(AA^{-1}=A^{-1}A=I\\)  
  矩阵的转置：设 A 为 m×n 阶矩阵（即 m 行 n 列）, A 的转置为n×m 阶矩阵 B，即 b (i,j)=a (j,i)，记 \\(A^{T}=B\\)(或\\(A^{'}=B\\)）  
  $$
    \begin{bmatrix}
          a \quad b \\
          c \quad d \\
          e \quad f 
    \end{bmatrix} ^{T}
  $$ =
  $$
    \begin{bmatrix}
          a \quad c \quad e \\
          b \quad d \quad f 
    \end{bmatrix}
  $$   
  矩阵的转置基本性质:  
  \\((A±B)^{T}=A^{T}±B^{T} \\)  
  \\((A×B)^{T}= B^{T}×A^{T}\\)  
  \\((A^{T})^{T}=A\\)  
  \\((KA)^{T}=KA^{T}\\)  
  matlab 中矩阵转置：\\(x=y^{'}\\)  

## 线性方程



    




