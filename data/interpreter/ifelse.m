a = 1;
x = 0;
y = 1;
while (a <= 10) {
    if (x == 0) {
        print 0;
        x = 1;
    }
    else {
        if (y == 1) {
            print 1;
            x = 0;
            y = 0;
        }
        else {
            print 2;
            x = 0;
            y = 1;
        }
    }
    a += 1;
}