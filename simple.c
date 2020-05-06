int f(int x) {
    return x*x;
}

int exp(int x, int y) {
    if (y == 0){
        print(y);
        return 1;
    }

    else
        return x*exp(x,y-1);
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

   if(x==3){
    print("hello")
   }
   print(exp(1,4));

}