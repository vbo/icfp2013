#include <stdint.h>
#include <string.h>
#include <stdlib.h>
#include <stdio.h>
#include "evaluator.h"

#define new_bv_program() (bv_program *)malloc(sizeof(bv_program))
#define alloc_args_for_program(p) (bv_program **)malloc(p->argc*sizeof(bv_program *))

// Public API

typedef enum {
    WAIT
} bv_parse_state_id;


typedef struct bv_parse_state {
    bv_parse_state_id state_id;

    char has_fold;
    char has_errors;
    int error_code;

    char id_str[30];
    char id2_str[30];
    char id3_str[30];

    bv_program *current;
} bv_parse_state;


static void _bv_parse(bv_parse_state *);


void bv_free(bv_program *bv)
{
    int i;

    //printf("FREE %p\n", bv);
    //printf("FREE %d\n", bv->operator_id);
    //printf("FREE %d\n", bv->argc);
    for (i = 0; i < bv->argc; i++)
    {
        bv_free(bv->args[i]);
    }

    if (bv->argc)
    {
        free(bv->args);
    }
    free(bv);
}


bv_program *bv_parse(char *formula)
{
    bv_program *program = (bv_program *)malloc(sizeof(bv_program));

    bv_parse_state state;

    state.has_errors = 0;
    state.has_fold = 0;
    state.error_code = 0;
    state.current = program;

    char *formula_to_parse = strdup(formula);

    // this returns lambda
    strtok(formula_to_parse, "(");

    // this returns first identifier
    char *id_str = strtok(NULL, "() ");
    strcpy(state.id_str, id_str);
    //printf("ID: %s\n", state.id_str);

    _bv_parse(&state);

    free(formula_to_parse);

    if (state.has_errors)
    {
        bv_free(program);
        return NULL;
    }

    return program;
}

// Implementation starts
typedef bv_int64 (*folder_func)(bv_int64, bv_int64);

const char ZERO_STR[] = "0";
const char ONE_STR[] = "1";

const char IF0_STR[] = "if0";
const char FOLD_STR[] = "fold";

const char XOR_STR[] = "xor";
const char OR_STR[] = "or";
const char AND_STR[] = "and";
const char PLUS_STR[] = "plus";

const char NOT_STR[] = "not";
const char SHL1_STR[] = "shl1";
const char SHR1_STR[] = "shr1";
const char SHR4_STR[] = "shr4";
const char SHR16_STR[] = "shr16";


void _bv_parse_fold(bv_parse_state *state)
{
    state->current->argc = 3;
    state->current->args = alloc_args_for_program(state->current);
    state->current->args[0] = new_bv_program();
    state->current->args[1] = new_bv_program();
    state->current->args[2] = new_bv_program();

    //printf("PARSE FOLD");

    bv_program *prev = state->current;

    state->current = prev->args[0];
    _bv_parse(state);

    state->current = prev->args[1];
    _bv_parse(state);

    // lambda
    strtok(NULL, "() ");

    strcpy(state->id2_str, strtok(NULL, "() "));
    strcpy(state->id3_str, strtok(NULL, "() "));

    //printf("ID2: %s\n", state->id2_str);
    //printf("ID3: %s\n", state->id3_str);

    state->has_fold = 1;
    state->current = prev->args[2];
    _bv_parse(state);
    state->has_fold = 0;

    state->current = prev;
}


void _bv_parse_unary(bv_parse_state *state)
{
    //printf("PARSE UNARY\n");
    state->current->argc = 1;
    state->current->args = alloc_args_for_program(state->current);
    state->current->args[0]  = new_bv_program();

    bv_program *prev = state->current;
    state->current = state->current->args[0];
    _bv_parse(state);
    state->current = prev;
}


void _bv_parse_binary(bv_parse_state *state)
{
    //printf("PARSE BINARY\n");
    state->current->argc = 2;
    state->current->args = alloc_args_for_program(state->current);
    state->current->args[0] = new_bv_program();
    state->current->args[1] = new_bv_program();

    bv_program *prev = state->current;

    state->current = prev->args[0];
    _bv_parse(state);
    state->current = prev->args[1];
    _bv_parse(state);

    state->current = prev;
}


void _bv_parse_if0(bv_parse_state *state)
{
    //printf("PARSE IF0\n");
    state->current->argc = 3;
    state->current->args = alloc_args_for_program(state->current);
    state->current->args[0] = new_bv_program();
    state->current->args[1] = new_bv_program();
    state->current->args[2] = new_bv_program();

    bv_program *prev = state->current;

    state->current = prev->args[0];
    _bv_parse(state);
    state->current = prev->args[1];
    _bv_parse(state);
    state->current = prev->args[2];
    _bv_parse(state);

    state->current = prev;
}


void _bv_parse(bv_parse_state *state)
{
    if (state->has_errors)
    {
        return;
    }

    char *op = strtok(NULL, "() ");
    //printf("PARSE OP: %s for %p\n", op, state->current);

    if (strcmp(op, FOLD_STR) == 0)
    {
        state->current->operator_id = FOLD;
        _bv_parse_fold(state);
    }
    else if (strcmp(op, IF0_STR) == 0)
    {
        state->current->operator_id = IF0;
        _bv_parse_if0(state);
    }
    /* Binary operators handling starts */
    else if (strcmp(op, XOR_STR) == 0)
    {
        state->current->operator_id = XOR;
        _bv_parse_binary(state);
    }
    else if (strcmp(op, OR_STR) == 0)
    {
        state->current->operator_id = OR;
        _bv_parse_binary(state);
    }
    else if (strcmp(op, AND_STR) == 0)
    {
        state->current->operator_id = AND;
        _bv_parse_binary(state);
    }
    else if (strcmp(op, PLUS_STR) == 0)
    {
        state->current->operator_id = PLUS;
        _bv_parse_binary(state);
    }
    /* Unary operators handling starts */
    else if (strcmp(op, NOT_STR) == 0)
    {
        state->current->operator_id = NOT;
        _bv_parse_unary(state);
    }
    else if (strcmp(op, SHL1_STR) == 0)
    {
        state->current->operator_id = SHL1;
        _bv_parse_unary(state);
    }
    else if (strcmp(op, SHR1_STR) == 0)
    {
        state->current->operator_id = SHR1;
        _bv_parse_unary(state);
    }
    else if (strcmp(op, SHR4_STR) == 0)
    {
        state->current->operator_id = SHR4;
        _bv_parse_unary(state);
    }
    else if (strcmp(op, SHR16_STR) == 0)
    {
        state->current->operator_id = SHR16;
        _bv_parse_unary(state);
    }
    /* Terminals handling starts */
    else if (strcmp(op, ZERO_STR) == 0)
    {
        state->current->operator_id = ZERO;
        state->current->argc = 0;
    }
    else if (strcmp(op, ONE_STR) == 0)
    {
        state->current->operator_id = ONE;
        state->current->argc = 0;
    }
    else if (strcmp(op, state->id_str) == 0)
    {
        state->current->operator_id = ID;
        state->current->argc = 0;
    }
    else if (state->id2_str && strcmp(op, state->id2_str) == 0)
    {
        state->current->operator_id = ID2;
        state->current->argc = 0;

        if (!state->has_fold)
        {
            state->has_errors = 1;
        }
    }
    else if (state->id3_str && strcmp(op, state->id3_str) == 0)
    {
        state->current->operator_id = ID3;
        state->current->argc = 0;

        if (!state->has_fold)
        {
            state->has_errors = 1;
        }
    }
}
