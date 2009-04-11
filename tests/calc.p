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
	
	WHILE i < 10 DO
	i := i + i;
	
	REPEAT
		i := i - 1
	UNTIL i < 0;
	
	for i := 1 to 10 do j := j + 2;
	
END.