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
END.