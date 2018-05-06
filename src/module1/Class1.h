#ifndef CLASS1_H
#define CLASS1_H

class Class1 {
public:
    explicit Class1(const int& x) : x(x) {}

    int getX() { return x; }

private:
    int x;
};

#endif //CLASS1_H
