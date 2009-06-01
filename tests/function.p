program test3; 
var 
	A : integer; 

	procedure ScopeInner; 
	var A : integer; 
		begin
		A := 10; 
		writeln(A) 
	end; 

	function Summation(num : integer) : integer;
	begin
		if num = 1 then 
			Summation := 1 
		else 
			Summation := 2;
	end; 

begin 
	A := 20; 
	writeln(A + 1 * 2); 
	ScopeInner;
	A := a + Summation(10);
	writeln(a);
	writeln(A); 
end.
