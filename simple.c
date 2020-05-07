int f(int x) {
    return x*x;
}

int exp(int x, int y) {
    if (y < 0)
        return 1;
    else
        return y+a(x,y);
}

int a(int x, int y) {
    if(y < 0)
        return 1;
    else
        return y+exp(x,y-1);
}
int main() {
   int x;
   float y;
   bool z;
   x = 55;
   y = 5/2;
   x = 5/2;
   print(exp(3,2));

}