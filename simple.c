int main() {

    int x;
    int y;
    bool z;

    x = 55;
    y = x * 8;
    z = true;

    print(z);

    while (x > 0) {
        if (x % 2 == 0)
            print(x);
        x = x - 1;
    }
}