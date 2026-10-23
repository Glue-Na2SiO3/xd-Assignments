package com.xuexi.shngji2;
import java.util.Scanner;
public class ComplexNumber implements Comparable<ComplexNumber> {
    private double real;
    private double imaginary;

    // 构造方法
    public ComplexNumber(double real, double imaginary) {
        this.real = real;
        this.imaginary = imaginary;
    }

    // 静态方法 valueOf(String str)
    public static ComplexNumber valueOf(String str) {
        // 这里简化处理，只处理形如 "real+imaginaryi" 的字符串
        String[] parts = str.trim().split("\\+");
        if (parts.length != 2) {
            throw new IllegalArgumentException("Invalid complex number format: " + str);
        }

        String realPart = parts[0];
        String imaginaryPart = parts[1].replaceAll("i", ""); // 移除 'i'

        try {
            double real = Double.parseDouble(realPart);
            double imaginary = Double.parseDouble(imaginaryPart);
            return new ComplexNumber(real, imaginary);
        } catch (NumberFormatException e) {
            throw new IllegalArgumentException("Invalid numeric format in complex number: " + str);
        }
    }

    // 实现 Comparable 接口的 compareTo 方法
    public int compareTo(ComplexNumber other) {
        // 假设我们按实部排序，如果实部相等则按虚部排序
        if (this.real != other.real) {
            return Double.compare(this.real, other.real);
        } else {
            return Double.compare(this.imaginary, other.imaginary);
        }
    }

    // 静态的加运算方法（简化处理，只处理两个复数相加）
    public static ComplexNumber add(ComplexNumber a, ComplexNumber b) {
        double real = a.real + b.real;
        double imaginary = a.imaginary + b.imaginary;
        return new ComplexNumber(real, imaginary);
    }

    // 其他的辅助方法，如 toString, getReal, getImaginary 等
    public String toString() {
        return real + "+" + imaginary + "i";
    }

    public double getReal() {
        return real;
    }

    public double getImaginary() {
        return imaginary;
    }
    public static void main(String[] args) {
        ComplexNumber c1 = ComplexNumber.valueOf("3+4i");
        ComplexNumber c2 = ComplexNumber.valueOf("1+2i");
        ComplexNumber sum = ComplexNumber.add(c1, c2);
        System.out.println("Sum: " + sum);
    }
}