int a(int x){
    return x;
}
int main() {
    int x;
    int y;


    x = 55;
    y = x * 8;

    print(a(1));
    while (x > 0) {
        if (x % 2 == 0)
            print(x);
        x = x - 1;
    }
}