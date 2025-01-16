a = 0;
b = 1;
while (b < 1000) {
    if (b == 3) {
        b += a;
        a = b - a;
        continue;
    }
    print b;
    b += a;
    a = b - a;
    if (b > 30) break;
}