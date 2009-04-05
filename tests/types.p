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
    c := "1";       { valid character assigned to variable c }
    c := 'd';       { valid character assigned to variable c }
    WRITELN(c);     { c contains the value 'd' }
END.