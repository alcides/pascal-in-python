PROGRAM calc;
VAR
	j : INTEGER;
	function hello(num : integer) : integer;
	begin
		hello := num + 1 * 2;
	end;
BEGIN

	j := 1;
	j := hello(j);
	WRITELN(j);
	WRITELN(1 / 3);
	WRITELN(4 div 3);
	WRITELN(5 mod 3);
END.