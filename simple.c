int f(int x) {
    return x*x;
}

int main() {
   int x;
   float y;
   bool z;
   x = f(33);  // <-- Need to add function call syntax

   // It is not hard to add function call syntax. It is just an identifier
   // followed by zero or more expressions separated by commas.

   y = x * 3.14;  // type checking. int * float is a float
   x = 3.14;      // convert to an int by truncating
   print(x)

   print("hello", f(33));

   print(f(f(33)));   // function composition should work
}