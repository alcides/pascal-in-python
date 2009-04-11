PROGRAM calc;
VAR
	j : REAL;
	i : INTEGER;
BEGIN
	j := 1 * 2;
	i := j * (1 + 2);
	if 1 > 2 then
	  i := i + 1
	else
	  i := i * 2;
END.