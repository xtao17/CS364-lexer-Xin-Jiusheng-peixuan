//(a == b) && (c == d)
//(a + b) > (c - d) && a || a || c
//print((a + b), "a", "b")
//a + b * d * (z + w) + -(a + b * c * (d + e))
int sum(int n,int a) {

 int sum;
 int i;

 a=1;
 if(a==1)
    print(n);
 sum = 0;
 i = 0;
 while (i < n) {
 if (i % 3 == 0 || i % 5 == 0)
    sum = sum + i;

 i = i + 1;
 }
 return sum;
}

int sum(int n) {
 int sum;
 int i;
 sum = 0;
 i = 0;
 while (i < n) {
 if (i % 3 == 0 || i % 5 == 0)
    sum = sum + i;

 i = i + 1;
 }
 return sum;
}