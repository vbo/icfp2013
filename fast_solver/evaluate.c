#include <stdio.h>

#include "evaluator.h"

int main(int argc, char**argv)
{
    if (argc != 2)
    {
        return 1;
    }

    char *formula = argv[1];
    bv_program *p = bv_parse(formula);
    printf("RESULT: %llu\n", bv_eval(p, 1));
    bv_free(p);

    return 0;
}
