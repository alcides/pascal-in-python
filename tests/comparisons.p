program Comparisons;
var
	a : INTEGER;
begin
		a := 1;
		WHILE a < 10 DO
		a := a + 1;
		writeint(a);
		
		if (a = 1 or a = 10) then writeln("cool");
end.
