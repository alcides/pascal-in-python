program Comparisons;
var
	a : INTEGER;
begin
	a := 1;
	if a = 1 and a = 2 and a = 3 then
		writeln(a)
	else
		writeln(2);
	writeln(3);
	
	for	a := 1 to 10 do
		writeln(a);
		
	while a > 1 do
	begin
		writeln(a);
		a := a - 1;
	end;
	repeat
	begin
		writeln(a);
		a := a * 2;
	end until a > 100;
	
end.
