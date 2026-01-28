package assignment_1;

public class LinkedListQuestions {
    
    // عقدة القائمة المرتبطة الأحادية
    static class Node {
        int data;
        Node next;
        
        Node(int data) {
            this.data = data;
            this.next = null;
        }
    }
    
    // عقدة القائمة المرتبطة الثنائية
    static class DoublyNode {
        int data;
        DoublyNode prev;
        DoublyNode next;
        
        DoublyNode(int data) {
            this.data = data;
            this.prev = null;
            this.next = null;
        }
    }
    
    // عقدة القائمة المرتبطة الدائرية
    static class CircularNode {
        int data;
        CircularNode next;
        
        CircularNode(int data) {
            this.data = data;
            this.next = null;
        }
    }
    
    // السؤال 6: تدوير قائمة مرتبطة إلى اليمين بمقدار k موقع
    public static Node rotateRight(Node head, int k) {
        if (head == null || head.next == null || k == 0) {
            return head;
        }
        
        // حساب طول القائمة
        Node current = head;
        int length = 1;
        while (current.next != null) {
            current = current.next;
            length++;
        }
        
        // جعل القائمة دائرية مؤقتاً
        current.next = head;
        
        // حساب الموضع الفعلي للتدوير
        k = k % length;
        int stepsToNewHead = length - k;
        
        // إيجاد الرأس الجديد
        current = head;
        for (int i = 1; i < stepsToNewHead; i++) {
            current = current.next;
        }
        
        Node newHead = current.next;
        current.next = null;
        
        return newHead;
    }
    
    // السؤال 8: إيجاد فهرس لقيمة معطاة في قائمة مرتبطة
    public static int findIndex(Node head, int value) {
        Node current = head;
        int index = 0;
        
        while (current != null) {
            if (current.data == value) {
                return index;
            }
            current = current.next;
            index++;
        }
        
        return -1; // القيمة غير موجودة
    }
    
    // السؤال 10: حذف العناصر المكررة من قائمة مرتبطة ثنائية
    public static DoublyNode removeDuplicates(DoublyNode head) {
        if (head == null || head.next == null) {
            return head;
        }
        
        DoublyNode current = head;
        
        while (current != null) {
            DoublyNode runner = current.next;
            
            while (runner != null) {
                if (runner.data == current.data) {
                    // حذف العقدة المكررة
                    if (runner.next != null) {
                        runner.next.prev = runner.prev;
                    }
                    if (runner.prev != null) {
                        runner.prev.next = runner.next;
                    }
                }
                runner = runner.next;
            }
            current = current.next;
        }
        
        return head;
    }
    
    // السؤال 12: البحث عن عنصر في قائمة مرتبطة ثنائية
    public static DoublyNode searchDoublyLinkedList(DoublyNode head, int value) {
        DoublyNode current = head;
        
        while (current != null) {
            if (current.data == value) {
                return current;
            }
            current = current.next;
        }
        
        return null; // العنصر غير موجود
    }
    
    // السؤال 14: حذف عقدة من موضع محدد في قائمة مرتبطة دائرية
    public static CircularNode deleteFromCircularList(CircularNode head, int position) {
        if (head == null) {
            return null;
        }
        
        // الحالة الخاصة: حذف العقدة الوحيدة
        if (head.next == head && position == 0) {
            return null;
        }
        
        CircularNode current = head;
        CircularNode prev = null;
        
        // إيجاد العقدة السابقة للرأس
        while (current.next != head) {
            current = current.next;
        }
        prev = current;
        current = head;
        
        // التنقل إلى الموضع المطلوب
        for (int i = 0; i < position; i++) {
            prev = current;
            current = current.next;
        }
        
        // تحديث الروابط
        if (current == head) {
            head = current.next;
        }
        
        prev.next = current.next;
        
        return head;
    }
    
    // السؤال 16: تقسيم قائمة مرتبطة دائرية إلى نصفين
    public static CircularNode[] splitCircularList(CircularNode head) {
        CircularNode[] halves = new CircularNode[2];
        
        if (head == null) {
            halves[0] = null;
            halves[1] = null;
            return halves;
        }
        
        // إيجاد منتصف القائمة باستخدام تقنية السلحفاة والأرنب
        CircularNode slow = head;
        CircularNode fast = head;
        
        while (fast.next != head && fast.next.next != head) {
            slow = slow.next;
            fast = fast.next.next;
        }
        
        // إذا كان عدد العقد زوجياً
        if (fast.next.next == head) {
            fast = fast.next;
        }
        
        // القائمة الأولى
        halves[0] = head;
        
        // القائمة الثانية
        if (head.next != head) {
            halves[1] = slow.next;
        } else {
            halves[1] = null;
        }
        
        // جعل القائمة الثانية دائرية
        fast.next = slow.next;
        
        // جعل القائمة الأولى دائرية
        slow.next = head;
        
        return halves;
    }
    
    // دالة مساعدة لعرض القائمة المرتبطة الأحادية
    public static void printLinkedList(Node head) {
        Node current = head;
        System.out.print("القائمة المرتبطة: ");
        while (current != null) {
            System.out.print(current.data + " → ");
            current = current.next;
        }
        System.out.println("null");
    }
    
    // اختبار الدوال
    public static void testLinkedListQuestions() {
        System.out.println("اختبار السؤال 6: تدوير القائمة المرتبطة");
        Node list = createSampleLinkedList();
        printLinkedList(list);
        list = rotateRight(list, 3);
        printLinkedList(list);
        
        System.out.println("\nاختبار السؤال 8: البحث عن عنصر");
        System.out.println("فهرس العنصر 7: " + findIndex(list, 7));
        System.out.println("فهرس العنصر 99: " + findIndex(list, 99));
        
        System.out.println("\nاختبار السؤال 10: حذف المكررات من قائمة ثنائية");
        DoublyNode doublyList = createSampleDoublyLinkedList();
        printDoublyLinkedList(doublyList);
        doublyList = removeDuplicates(doublyList);
        System.out.print("بعد حذف المكررات: ");
        printDoublyLinkedList(doublyList);
        
        System.out.println("\nاختبار السؤال 12: البحث في قائمة ثنائية");
        DoublyNode found = searchDoublyLinkedList(doublyList, 3);
        System.out.println("العنصر 3 موجود: " + (found != null));
        
        System.out.println("\nاختبار السؤال 14: حذف من قائمة دائرية");
        CircularNode circularList = createSampleCircularLinkedList();
        System.out.print("القائمة الدائرية الأصلية: ");
        printCircularLinkedList(circularList, 10);
        circularList = deleteFromCircularList(circularList, 2);
        System.out.print("بعد حذف الموضع 2: ");
        printCircularLinkedList(circularList, 10);
        
        System.out.println("\nاختبار السؤال 16: تقسيم قائمة دائرية");
        CircularNode[] halves = splitCircularList(circularList);
        System.out.print("النصف الأول: ");
        printCircularLinkedList(halves[0], 5);
        System.out.print("النصف الثاني: ");
        printCircularLinkedList(halves[1], 5);
    }
    
    // دوال مساعدة لإنشاء قوائم عينة
    private static Node createSampleLinkedList() {
        Node head = new Node(1);
        head.next = new Node(2);
        head.next.next = new Node(3);
        head.next.next.next = new Node(4);
        head.next.next.next.next = new Node(5);
        head.next.next.next.next.next = new Node(6);
        head.next.next.next.next.next.next = new Node(7);
        return head;
    }
    
    private static DoublyNode createSampleDoublyLinkedList() {
        DoublyNode head = new DoublyNode(1);
        DoublyNode node2 = new DoublyNode(2);
        DoublyNode node3 = new DoublyNode(3);
        DoublyNode node4 = new DoublyNode(2);
        DoublyNode node5 = new DoublyNode(4);
        DoublyNode node6 = new DoublyNode(3);
        
        head.next = node2;
        node2.prev = head;
        node2.next = node3;
        node3.prev = node2;
        node3.next = node4;
        node4.prev = node3;
        node4.next = node5;
        node5.prev = node4;
        node5.next = node6;
        node6.prev = node5;
        
        return head;
    }
    
    private static CircularNode createSampleCircularLinkedList() {
        CircularNode head = new CircularNode(1);
        CircularNode node2 = new CircularNode(2);
        CircularNode node3 = new CircularNode(3);
        CircularNode node4 = new CircularNode(4);
        CircularNode node5 = new CircularNode(5);
        
        head.next = node2;
        node2.next = node3;
        node3.next = node4;
        node4.next = node5;
        node5.next = head;
        
        return head;
    }
    
    private static void printDoublyLinkedList(DoublyNode head) {
        DoublyNode current = head;
        System.out.print("null ↔ ");
        while (current != null) {
            System.out.print(current.data + " ↔ ");
            current = current.next;
        }
        System.out.println("null");
    }
    
    private static void printCircularLinkedList(CircularNode head, int maxNodes) {
        if (head == null) {
            System.out.println("قائمة فارغة");
            return;
        }
        
        CircularNode current = head;
        int count = 0;
        System.out.print("↻ ");
        do {
            System.out.print(current.data + " → ");
            current = current.next;
            count++;
        } while (current != head && count < maxNodes);
        System.out.println("↺ (العودة للبداية)");
    }
}