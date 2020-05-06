int f(int x) {
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
   x = 55;
   y = 5;
   while (x > 0) {
        if (x % 2 == 0){
            print(x);
            print(x+x);
        }

        x = x - 1;
    }
   print(y);
   print(3**2**3);
   print(exp(2,3));
   print(f(f(33)));

}