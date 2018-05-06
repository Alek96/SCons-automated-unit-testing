#include "third_party/catch.hpp"
#include "../Class1.h"

TEST_CASE("Class1Test","[Class1]") {
    Class1 class1(2);
    REQUIRE(class1.getX() == 2);
}
