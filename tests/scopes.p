PROGRAM calc;
VAR
	j : INTEGER;
	i : INTEGER;
BEGIN
	j := 1;

	BEGIN
		WRITEINT(j);
		j := j + 1;
		WRITEINT(j);
	END;

	j := j + 1;

	WRITEINT(j);

END.