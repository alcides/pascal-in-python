program Comparisons;
var
	a : INTEGER;
begin
	a := 1;
	repeat
		begin
		a := a + 1;
		writeint(a);
		end
	until a < 10;
end.
