#include "third_party/catch.hpp"
#include "../Class2.h"

TEST_CASE("Class2Test","[Class2]") {
    Class2 class2(2);
    REQUIRE(class2.getX() == 2);
}
