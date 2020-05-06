int a(int x, int y){
    return x+y;
}
int main() {
    int x;
    int y;


    x = 55;
    y = x * 8;

    print(a(1, 2));
    while (x > 0) {
        if (x % 2 == 0)
            print(x);
        x = x - 1;
    }
}