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
   z=true;
   print(z+1);
   // It is not hard to add function call syntax. It is just an identifier
   // followed by zero or more expressions separated by commas.
}