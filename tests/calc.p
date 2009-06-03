PROGRAM calc;
VAR
	j : INTEGER;
	function add(num : integer, num2 : integer, t2 :real) : integer;
	begin
		writeln(t2);
		add := num + num2;
	end;
BEGIN
	j := 1;
	j := add(j,2,5.0);
	WRITELN(j);
	WRITELN(1.0 / 3.0);
	WRITELN(4 div 3);
	WRITELN(5 mod 3);
END.