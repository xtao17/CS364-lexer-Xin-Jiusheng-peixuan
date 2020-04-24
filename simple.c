//(a == b) && (c == d)
//(a + b) > (c - d) && a || a || c
//print((a + b), "a", "b")
//a + b * d * (z + w) + -(a + b * c * (d + e))
int sum_3_or_5(int n) {
 int sum;
 int i;
 sum = 0;
 n = 0;
 while (i < n) {
 if (i % 3 == 0 || i % 5 == 0)
 sum = sum + i;

 i = i + 1;
 }
 return sum;
}
int sum() {

 print("The answer is: ", sum_3_or_5(1000 || n));
}
