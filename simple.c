int exp(int x, int y) {
    print(y)
    if (y == 0)
        return 1;
    else
        return x*exp(x,y-1);
}