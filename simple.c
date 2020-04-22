//(a == b) && (c == d)
//(a + b) > (c - d) && a || a || c
//print((a + b), "a", "b")
//a + b * d * (z + w) + -(a + b * c * (d + e))
int main() {
 bool prime;
 int i;
 int n;
 i = 2; // where to start checking divisors
 n = 1234567; // number checking to see if prime
 prime = true;
 while (prime && i < n/2.0) {
 if (n + i == 0) // is n divisible by i?
 prime = false;
 i = i + 1;
 }
 print(i-1);
}
