grammar Jertl;

options {
   language = Python3;
}

transform
   : structure IMPLIES structure
   ;

collation
   : matcher*
   ;

rule_
   : matcher* IMPLIES setter*
   ;

matcher
   : variable MATCHES structure
   ;

setter
   : variable ASSIGNED structure
   ;

IMPLIES
   : '-->'
   ;

// Structures

structure
   : obj
   | array
   | atom
   | variable
   ;

obj
   : '{' key_values+=key_value (',' key_values+=key_value)* (',' kwargs)?'}'
   | '{' '}'
   ;

key_value
   : STRING ':' structure
   ;

kwargs
   : '**' variable
   ;

array
   : '[' elements+=element (',' elements+=element)* ']'
   | '[' ']'
   ;

element
   : structure
   | varargs
   ;

varargs
   : '*' variable
   ;

atom
   : NULL
   | TRUE
   | FALSE
   | INTEGER
   | FLOAT
   | STRING
   ;

variable
   : IDENTIFIER
   ;

NULL
   : 'null'
   ;
TRUE
   : 'true'
   ;

FALSE
   : 'false'
   ;

STRING
   : '"' (ESC | SAFECODEPOINT)* '"'
   ;
MATCHES
   : '~'
   ;

ASSIGNED
   : ':='
   ;

IDENTIFIER
   : VALID_ID_START VALID_ID_CHAR*
   ;

fragment VALID_ID_START
   : ('a' .. 'z') | ('A' .. 'Z') | '_'
   ;

fragment VALID_ID_CHAR
   : VALID_ID_START | ('0' .. '9')
   ;

fragment ESC
   : '\\' (["\\/bfnrt] | UNICODE)
   ;

fragment UNICODE
   : 'u' HEX HEX HEX HEX
   ;

fragment HEX
   : [0-9a-fA-F]
   ;

fragment SAFECODEPOINT
   : ~ ["\\\u0000-\u001F]
   ;

INTEGER
   : '-'? INT
   ;

FLOAT
   : '-'? INT ('.' [0-9] +)? EXP?
   ;

fragment INT
   : '0' | [1-9] [0-9]*
   ;

// no leading zeros

fragment EXP
   : [Ee] [+\-]? INT
   ;

// \- since - means "range" inside [...]

WS
   : [ \t\n\r] + -> skip
   ;

LINE_COMMENT
    : '//' ~[\r\n]* -> skip
    ;
