#include "third_party/catch.hpp"
#include "../Class1_1.h"

TEST_CASE("Class1_1Test","[Class1][Class1_1]") {
    Class1_1 class1(2);
    REQUIRE(class1.getX() == 2);
}
