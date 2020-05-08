int f(int x) {
    return x*x;
}

int exp(int x, int y) {
    if (y == 0)
        return 1;
    else
        return x*exp(x,y-1);
}

int a(int x, int y) {
    if(y == 0)
        return 1;
    else
        return x*a(x,y-1);
}
int main() {
   int x=5;
   float y;
   bool z;

   y = 5/2;

   print(a(3,2));
   print(x)
   print("hello");
   print("hi", a(4, 5));
   print(3**2**3*2+4-5*2/2);

}