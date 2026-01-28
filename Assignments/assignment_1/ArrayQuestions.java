package assignment_1;

import java.util.Arrays;
import java.util.Random;

public class ArrayQuestions {
    
    // السؤال 2: حذف عنصر عشوائي من مصفوفة
    public static int[] removeRandomElement(int[] arr) {
        if (arr.length == 0) {
            return new int[0];
        }
        
        Random rand = new Random();
        int randomIndex = rand.nextInt(arr.length);
        
        int[] newArray = new int[arr.length - 1];
        int newIndex = 0;
        
        for (int i = 0; i < arr.length; i++) {
            if (i != randomIndex) {
                newArray[newIndex++] = arr[i];
            }
        }
        
        return newArray;
    }
    
    // السؤال 4: عكس ترتيب عناصر مصفوفة
    public static void reverseArray(int[] arr) {
        int start = 0;
        int end = arr.length - 1;
        
        while (start < end) {
            // تبديل العناصر
            int temp = arr[start];
            arr[start] = arr[end];
            arr[end] = temp;
            
            start++;
            end--;
        }
    }
    
    // دالة مساعدة لعرض المصفوفة
    public static void printArray(int[] arr, String message) {
        System.out.print(message + ": [");
        for (int i = 0; i < arr.length; i++) {
            System.out.print(arr[i]);
            if (i < arr.length - 1) {
                System.out.print(", ");
            }
        }
        System.out.println("]");
    }
    
    // اختبار الدوال
    public static void testArrayQuestions() {
        int[] originalArray = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
        
        // اختبار السؤال 2
        printArray(originalArray, "المصفوفة الأصلية");
        int[] arrayAfterRemoval = removeRandomElement(originalArray);
        printArray(arrayAfterRemoval, "بعد حذف عنصر عشوائي");
        
        // اختبار السؤال 4
        int[] arrayToReverse = originalArray.clone();
        printArray(arrayToReverse, "قبل العكس");
        reverseArray(arrayToReverse);
        printArray(arrayToReverse, "بعد العكس");
    }
}