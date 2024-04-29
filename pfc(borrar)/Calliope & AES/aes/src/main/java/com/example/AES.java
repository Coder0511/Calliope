package com.example;

public class AES {
    public static void main( String[] args ) {
        String plainText = "This is a message we will encrypt with AES!";
        int[] key = new int[]{1, 2, 3, 4,
                                5, 6, 7, 8,
                                9, 10, 11, 12,
                                13, 14, 15, 16};

        aesEncrypt(plainText, key);
    }
}