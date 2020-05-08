int f(int x) {
    return x*x;
}

int exp(int x, int y) {
    if (y == 0)
        return 1;
    else
        return x*exp(x,y-1);
}

float a(int x, int y) {
    if(y == 0)
        return 1;
    else
        return x*b(x,y-1);
}
int main() {
   int x;
   float y;
   bool z;
   x = 55;
   y = 5/2;
   x = 5/2;
   print(a(3,2));

}