package com.xuexi.shngji2;
import java.util.Scanner;
class My_Complex{
    private double real;
    private double imaginary;

    // 构造函数
    public My_Complex(double real, double imaginary) {
        this.real = real;
        this.imaginary = imaginary;
    }
    // 构造函数，依据基本数值类型值构建复数对象实例
    public My_Complex(double real) {
        this(real, 0);
    }
    // 复数加法
    public My_Complex add(My_Complex c) {
        return new My_Complex(this.real + c.real, this.imaginary + c.imaginary);
    }
    // 复数减法
    public My_Complex subtract(My_Complex c) {
        return new My_Complex(this.real - c.real, this.imaginary - c.imaginary);
    }
    // 复数乘法
    public My_Complex multiply(My_Complex c) {
        double realPart = this.real * c.real - this.imaginary * c.imaginary;
        double imaginaryPart = this.real * c.imaginary + this.imaginary * c.real;
        return new My_Complex(realPart, imaginaryPart);
    }
    // 复数除法
    public My_Complex divide(My_Complex c) {
        double denominator = c.real * c.real + c.imaginary * c.imaginary;
        double realPart = (this.real * c.real + this.imaginary * c.imaginary) / denominator;
        double imaginaryPart = (this.imaginary * c.real - this.real * c.imaginary) / denominator;
        return new My_Complex(realPart, imaginaryPart);
    }
    // 重写equals方法
    public boolean equals(My_Complex obj) {
        return Double.compare(obj.real, real) == 0 &&
                Double.compare(obj.imaginary, imaginary) == 0;
    }
    // 重写toString方法
    public String toString() {
        return "(" + real + " + " + imaginary + "i)";
    }
    // 获取实部
    public double getReal() {
        return real;
    }
    // 获取虚部
    public double getImaginary() {
        return imaginary;
    }
}
public class ComplexTest {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        System.out.println("Enter real part for the first complex number:");
        double real1 = scanner.nextDouble();
        System.out.println("Enter imaginary part for the first complex number:");
        double imaginary1 = scanner.nextDouble();
        System.out.println("Enter real part for the second complex number:");
        double real2 = scanner.nextDouble();
        System.out.println("Enter imaginary part for the second complex number:");
        double imaginary2 = scanner.nextDouble();
        My_Complex c1 = new My_Complex(real1, imaginary1);
        My_Complex c2 = new My_Complex(real2, imaginary2);
        System.out.println("Addition: " + c1.add(c2));
        System.out.println("Subtraction: " + c1.subtract(c2));
        System.out.println("Multiplication: " + c1.multiply(c2));
        System.out.println("Division: " + c1.divide(c2));
        System.out.println("Is_equal: " + c1.equals(c2));
        System.out.println("real1:"+c1.getReal()+";imaginary1:"+c1.getImaginary());
        System.out.println("real2:"+c2.getReal()+";imaginary2:"+c2.getImaginary());

        scanner.close();
    }
}
