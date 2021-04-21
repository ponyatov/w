// original:
// https://github.com/yzyzsun/truffle-erlang/blob/master/src/main/antlr/me/yzyzsun/jiro/parser/CoreErlang.g4

grammar CoreErlang;

module
    : 'module' ATOM
    REST
    ;

INTEGER            : SIGN? DIGIT+ ;
ATOM               : '\'' NAME '\'' ;
NAME               : NAME_CHAR ( NAME_CHAR | DIGIT )* ;

fragment SIGN      : '+' | '-' ;
fragment DIGIT     : [0-9] ;
fragment UPPER     : [A-Z] ;
fragment LOWER     : [a-z] ;
fragment NAME_CHAR : UPPER | LOWER | '_' ;

WHITESPACE         : [ \t\r\n]    -> skip ;
COMMENT            : '%' ~[\r\n]* -> skip ;
REST               : .* ;
