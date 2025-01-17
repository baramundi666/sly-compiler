E1 = [ [ 1, 2, 3],
        [ 4, 5, 6],
       [ 7, 8, 9],
        [ 10, 11, 12] ];
print "E1:", E1;
X = [1.0, 2.5, 3.14];
print X;
 Y = X';
 print "X transposed:", Y;
 Y[0, 0] = 99.0;
 print Y;
 Y[0, 0] = 2 / 1.0;
 z = Y[1, 0] + 5;
 W = ones(1, 3) .+ ones(1, 3);
 print 'X/(2*ones)', X./W;
 print 'Y, z:', Y, z;