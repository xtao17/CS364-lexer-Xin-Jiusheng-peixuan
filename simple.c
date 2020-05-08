int f(int x) {
    print(1);
    return x*x;
}

int exp(int x, int y) {

    if (y == 0)
        return 1;
    else
        return x*exp(x,y-1);
}

int main() {
   int x;
   float y;
   bool z;
   x = 33;

   // It is not hard to add function call syntax. It is just an identifier
   // followed by zero or more expressions separated by commas.

   y = x * 3.14;  // type checking. int * float is a float
   x = 3.14;      // convert to an int by truncating
   z = true;
   print(f(x))
   print(exp(3, 3))
   x = 55;
   while (x > 0) {
        if (x % 2 == 0)
            print(x);
        x = x - 1;
    }
}