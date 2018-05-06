#ifndef CLASS1_1_H
#define CLASS1_1_H

class Class1_1 {
public:
    explicit Class1_1(const int& x) : x(x) {}

    int getX() { return x; }

private:
    int x;
};

#endif //CLASS1_H
