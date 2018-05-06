#ifndef CLASS2_H
#define CLASS2_H

class Class2 {
public:
    explicit Class2(const int& x) : x(x) {}

    int getX() { return x; }

private:
    int x;
};

#endif //CLASS1_H
