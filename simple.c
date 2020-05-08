int exp(int x, int y) {
    print(y);
    if (y == 0)
        return 1;
    else
        return x*exp(x,y-1);
}

int main() {
   int y=33;
   int x = y * 99;

   print(exp(2, 10));

}