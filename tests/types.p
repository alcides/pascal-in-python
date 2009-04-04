PROGRAM types;
VAR
   x : REAL;
   i : INTEGER;
   c : CHAR;        { variable name is c, type is character }
   s : STRING(255);      { variable name is s, type is string }
BEGIN
    x := -34.55;    { valid real number assigned to variable x }
    x := -3.9E-3;   { valid real number assigned to variable x }
    WRITELN(x);     { x contains the value -3.9E-3 }
    i := 10;        { valid integer number assigned to variable i }
    i := i * i;     { valid (!) - i will be 100 now }
    i := 9933;      { valid integer number assigned to variable i }
    i := -99999;    { invalid integer - too small }
    { i := 999.44;    { invalid assignment - types do not match }
    c := '1';       { valid character assigned to variable c }
    { c := 1;         { invalid assignment - types do not match }
    { c := 'Bert';    { invalid assignment - types do not match }
    c := 'd';       { valid character assigned to variable c }
    WRITELN(c);     { c contains the value 'd' }
    { d := 'c';       { unknown variable - the variable d is not declared }
    { WRITELN(s);     { invalid reference - s has undefined value }
END.