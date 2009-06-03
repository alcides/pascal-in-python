program testvar; 
var 
y : real;  
z : real;
a : string;
c : integer;

procedure ScopeInner2(s : integer);
var K : char;
begin
    writeln(s);
end;

procedure ScopeInner(i: integer);
var K : char;
begin
    writeln(i);
    i := i +1;
    ScopeInner2(i);
end;

function Add(j:iNteger): intEger;
begin
       Add := 1 + j;
    ScopeInner2(j);
end;

procedure Sco;
var P : integer;
Q: real; 
z: real;
begin
    P := 10 + c;
    z := 4.4;
    Q := 2.2 * z;    
    writeln(P);
    P := Add(P);
    ScopeInner(P);
end;

begin 
       z := 2.2;
      y := 1.3 + z;
      c := 2 + 5*2 + 4 mod 7 div 6;
      write('O mod z e: ');
      writeln(y);
      writeln(c);
    Sco;
    ScopeInner(c);
	c := c +1;
    ScopeInner(c);
    c := Add(2);
    writeln(c);
end.