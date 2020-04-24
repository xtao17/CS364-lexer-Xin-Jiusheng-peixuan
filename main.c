// Test #1 Euler project problem 1

int sum_3_or_5(int n) {

int sum;
int i;
sum = 0;
 i = 0;

while (i < n) {

    if (i % 3 == 0 || i % 5 == 0)
    sum = sum + i; i = i + 1;

}

return sum;

}
 //print("The answer is: ", sum_3_or_5(1000), "Woot!");

int main(int u) {
int i;
}
// Test #2 A program that determines if // a number n is prime
int main() {

    bool prime; int i;
    int n;
    i = 2;
    n = 1234567; prime = true;
    // where to start checking divisors
    // number checking to see if prime

    while (prime || i < n/2.0) {

        if(n%i==0) //is n divisible by i?
            prime = false;
        i=i+1;
     }

    print(i-1);
}